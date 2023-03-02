# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


import re
import time
import miaou.logger as logger
from miaou.scanner.base import Scanner
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


_step_interval = 2


class SeleniumScanner(Scanner):
    """selenium scanner"""

    def __init__(self, config):
        """initializer"""

        if "firefox" == config.get("driver", "chrome"):
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()

        wait_timeout = config.get("wait_timeout", 3)
        self.driver.implicitly_wait(wait_timeout)
        self.wait = WebDriverWait(self.driver, wait_timeout)

    def open(self, site_url, username, password):
        """login zentao"""

        logger.stage("login zentao '%s'" % site_url)

        self.driver.get(site_url)
        time.sleep(_step_interval)

        account = self._wait_for_element("input#account")
        account.send_keys(username)

        passwd = self._wait_for_element("input[name=password]")
        passwd.send_keys(password)

        auth = self._wait_for_element("button#submit")
        # auth.send_keys(Keys.ENTER)
        auth.click()

        time.sleep(_step_interval)

    def close(self):
        """close scanner"""

        self.driver.close()

    def get_module_groups(self, dev_url):
        """get module group page urls

        return url string list
        """

        urls = []

        self.driver.get(dev_url)
        time.sleep(_step_interval)

        # check out iframe
        self._switch_to_content_iframe()

        # find module group urls
        mg_elements = self._wait_for_elements(
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
        self.driver.get(api_url)
        time.sleep(_step_interval)

        # check out iframe
        self._switch_to_content_iframe()

        # find urls
        detail_elements = self._wait_for_elements(
            "#mainContent .main-col.main-content .detail")
        for element in detail_elements:
            url = element.find_element(By.CSS_SELECTOR, ".detail-title").text

            method, path, params = self._parse_url_to_api_items(url)
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
            ifr = self._wait_for_element(
                "iframe#appIframe-admin, iframe#appIframe-my")
            self.driver.switch_to.frame(ifr)
        except Exception:
            pass

    def _wait_for_element(
        self,
        selector,
        scroll_to=True,
        by=By.CSS_SELECTOR
    ):
        """wait for element, scroll window to the element position
        if scroll_to is True, make the element visible.
        """

        try:
            _element = self.wait.until(
                lambda driver: driver.find_element(by, selector))

            if scroll_to:
                self._scroll_to_element(_element)
        except Exception:
            logger.warning("element not found %s" % selector)
            _element = None
        return _element

    def _wait_for_elements(
        self,
        selector,
        by=By.CSS_SELECTOR
    ):
        """wait for elements by selector type"""

        return self.wait.until(
            lambda driver: driver.find_elements(by, selector))

    def _element_exists(
        self,
        selector,
        by=By.CSS_SELECTOR
    ):
        """check out the element existence"""

        try:
            _element = self.wait.until(
                lambda driver: driver.find_element(by, selector))
        except Exception:
            _element = None

        if _element is not None:
            logger.info("element found %s" % selector)
            return True
        else:
            logger.info("element not exists %s" % selector)
            return False

    def _scroll_to_element(self, element):
        """scroll window to the element position"""

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )

    def _parse_url_to_api_items(self, url):
        """parse url to api items,
        return tuple contains (method, path, params)"""

        logger.info("parsing '%s'" % url)

        path = []
        params = []

        # remove namespace and suffix
        slices = re.split("\s+", url)
        method = slices[0].strip().upper()
        if "GET/POST" == method:
            method = "POST"

        url = slices[1].strip()
        for pattern in (
            r"^/zentao/",
            r"\.json.*$",
        ):
            url = re.sub(pattern, "", url)

        # split path
        for t in url.split("-"):
            t = t.strip()
            if re.match("\[\w+\]", t) is None:
                logger.info("- got path '%s'" % t)
                path.append(t)
            else:
                t = t.replace(r"[", "")
                t = t.replace(r"]", "")
                logger.info("- got param '%s'" % t)
                params.append(t)

        return (method, "-".join(path), params)
# end
