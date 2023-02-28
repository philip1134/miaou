# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


import time
import miaou.logger as logger
import miaou.utils as utils
from miaou.scanner.selenium_wrapper import SeleniumWrapper


class SeleniumScanner:
    """selenium scanner"""

    def __init__(self):
        """initializer"""

        self.selenium = SeleniumWrapper()

    def open(self, site_url, username, password):
        """login zentao"""

        logger.stage("login zentao '%s'" % site_url)
        self.selenium.driver.get(site_url)
        time.sleep(2)

        account = self.selenium.wait_for_element("input#account")
        account.send_keys(username)

        passwd = self.selenium.wait_for_element("input[name=password]")
        passwd.send_keys(password)

        auth = self.selenium.wait_for_element("button#submit")
        # auth.send_keys(Keys.ENTER)
        auth.click()

    def close(self):
        """close scanner"""

        self.selenium.close()

    def get_module_groups(self, dev_url):
        """get module group page urls

        return url string list
        """

        urls = []

        self.selenium.driver.get(dev_url)
        time.sleep(2)

        # check out iframe
        self._switch_to_content_iframe()

        # find module group urls
        mg_elements = self.selenium.wait_for_elements(
            "#mainContent #sidebar a")
        for element in mg_elements:
            url = element.get_attribute("href")
            logger.info("got '%s'" % url)
            urls.append(url)

        return urls

    def get_apis(self, api_url):
        """get apis from api page

        return list like [{name, method, path, params}]
        """

        apis = []

        logger.info("get api from '%s'..." % api_url)
        self.selenium.driver.get(api_url)
        time.sleep(1)

        # check out iframe
        self._switch_to_content_iframe()

        # find urls
        detail_elements = self.selenium.wait_for_elements(
            "#mainContent .main-col.main-content .detail")
        for element in detail_elements:
            url = element.find_element_by_css_selector(
                ".detail-title").text

            method, path, params = utils.parse_url_to_api_items(url)
            name = path.replace("-", "_")

            apis.append({
                "name": name,
                "method": method,
                "path": path,
                "params": params
            })

        return apis

# private
    def _switch_to_content_iframe(self):
        """check out the iframe exists and switch into it"""

        try:
            logger.info("check out iframe...")
            ifr = self.selenium.wait_for_element(
                "iframe#appIframe-admin, iframe#appIframe-my")
            self.selenium.driver.switch_to.frame(ifr)
        except Exception:
            pass

# end
