# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-03-02
#


import re
import json
import urllib
import requests
import miaou.logger as logger
from miaou.scanner.base import Scanner


class ApiScanner(Scanner):
    """scan specs by zentao apis"""

    def __init__(self, config):
        """initializer"""

        pass

    def open(self, site_url, username, password):
        """tear up works"""

        session_url = urllib.parse.urljoin(
            site_url, "zentao/api-getSessionID.json")
        login_url = urllib.parse.urljoin(
            site_url, "zentao/user-login.json")

        return self._get_session(session_url) and \
            self._login(login_url, username, password)

    def get_module_groups(self, dev_url):
        """get module group page urls

        return url string list [url]
        """

        urls = []

        # change html to json
        dev_json_url = re.sub(r"\.html.*", r".json", dev_url)
        api_url_prefix = re.sub(r"\.html.*", "", dev_url)

        response = requests.get(
            dev_json_url,
            params={self.session_name: self.session_id}
        ).json()

        if "success" == response.get("status"):
            data = json.loads(response.get("data", r"{}"))

            # get modules, it's a dict like
            #   {module_name: {api_name: api_name}}
            modules = data.get("modules", {})

            # get apis
            for module, apis in modules.items():
                if isinstance(apis, dict):
                    _apis = apis.keys()
                elif isinstance(apis, list):
                    _apis = apis
                else:
                    _apis = []
                    logger.warning(
                        "unknown apis data type of module '%s'" % module)

                for api_name in _apis:
                    api = "%s-%s.json" % (api_url_prefix, api_name)
                    urls.append(api)
                    logger.info("got '%s'" % api)

        else:
            logger.error("fail to get module groups")

        return urls

    def get_apis(self, api_url):
        """get apis from api page

        return list like [{name, method, path, params}]
        """

        apis = []

        response = requests.get(
            api_url,
            params={self.session_name: self.session_id}
        ).json()

        if "success" == response.get("status"):
            data = json.loads(response.get("data", r"{}"))

            # selected module, it's api prefix
            module = data.get("selectedModule", "")

            # get apis, it's a list like
            #   [{name, post, param, desc...}]
            responded_apis = data.get("apis", [])
            for responded_api in responded_apis:
                api = {}

                # api name
                name = responded_api.get("name", "")

                api["name"] = "%s_%s" % (module, name)
                logger.info("got name: %s" % api["name"])

                # api path
                api["path"] = "%s-%s" % (module, name)
                logger.info("- got path: %s" % api["path"])

                # api method
                if responded_api.get("post", False):
                    api["method"] = "POST"
                else:
                    api["method"] = "GET"

                # api params
                params = responded_api.get("param", [])
                if isinstance(params, dict):
                    api["params"] = list(params.keys())
                    logger.info("- got params: %s" % api["params"])
                else:
                    api["params"] = []

                apis.append(api)
        else:
            logger.error("fail to get api from '%s'" % api_url)

        return apis

# protected
    def _get_session(self, session_url):
        """get zentao session name and session id"""

        response = requests.get(session_url).json()

        if "success" == response.get("status"):
            # get data list and return to caller
            session = json.loads(response["data"])
            self.session_name = session["sessionName"]
            self.session_id = session["sessionID"]

            logger.info("got session")
            return True
        else:
            # fail to get session
            logger.error("fail to get session")
            return False

    def _login(self, login_url, username, password):
        """login zentao with username and password"""

        response = requests.post(
            login_url,
            params={
                "account": username,
                "password": password,
                self.session_name: self.session_id
            }
        ).json()

        if "success" == response.get("status"):
            logger.info("succeed to login zentao")
            return True
        else:
            # fail to sign in
            logger.error("fail to login zentao")
            return False

# end
