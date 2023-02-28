# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-07-18
#


import time
import miaou.logger as logger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


WD_FIND_ELEMENT_FUNC = {
    "css": "css_selector",
    "xpath": "xpath",
    "class": "class_name",
    "id": "id",
    "tag": "tag_name",
    "name": "name",
    "partial": "partial_link_text",
    "link": "link_text",
}

step_interval = 5


class SeleniumWrapper:
    """selenium wrapper"""

    def __init__(self, driver="chrome"):
        super(SeleniumWrapper, self).__init__()

        if "firefox" == driver:
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()

        self.driver.implicitly_wait(3)
        self.wait = WebDriverWait(self.driver, 3)

    def close(self):
        """close performer environment."""

        self.driver.quit()

    def wait_for_element(
        self,
        selector,
        scroll_to=True,
        by="css"
    ):
        """wait for element, scroll window to the element position
        if scroll_to is True, make the element visible.
        supported css selector types:
            css:        find_element_by_css_selector
            xpath:      find_element_by_xpath
            class:      find_element_by_class_name
            id:         find_element_by_id
            tag:        find_element_by_tag_name
            name:       find_element_by_name
            partial:    find_element_by_partial_link_text
            link:       find_element_by_link_text
        """
        try:
            _element = self.wait.until(
                lambda driver: getattr(
                    driver,
                    self.__get_webdriver_func(by, False))(selector))

            if scroll_to:
                self.scroll_to_element(_element)
        except Exception:
            logger.warning("element not found %s" % selector)
            _element = None
        return _element

    def wait_for_elements(
        self,
        selector,
        by="css"
    ):
        """wait for elements by css selector type, supported types:
            css:        find_elements_by_css_selector
            xpath:      find_elements_by_xpath
            class:      find_elements_by_class_name
            id:         find_elements_by_id
            tag:        find_elements_by_tag_name
            name:       find_elements_by_name
            partial:    find_elements_by_partial_link_text
            link:       find_elements_by_link_text
        """
        return self.wait.until(lambda driver: getattr(driver,
                               self.__get_webdriver_func(by, True))(selector))

    def element_exists(self, selector, by="css"):
        """check out the element existence"""
        try:
            _element = self.wait.until(lambda driver: getattr(
                driver,
                self.__get_webdriver_func(by, False))(selector))
        except Exception:
            _element = None

        if _element is not None:
            logger.info("element found %s" % selector)
            return True
        else:
            logger.info("element not exists %s" % selector)
            return False

    def scroll_to_element(self, element):
        """scroll window to the element position"""

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )

    def switch_window(
        self,
        index,
        page_name
    ):
        self.driver.switch_to_window(self.driver.window_handles[index])
        logger.info("switch to page %s" % page_name)
        time.sleep(step_interval)

# private
    @staticmethod
    def __get_webdriver_func(
        selector_type,
        find_group=False
    ):
        """get webdriver function name by selector type"""

        if selector_type not in WD_FIND_ELEMENT_FUNC:
            selector_type = "css"

        if find_group:
            func_name = "find_elements_by_{0}".format(
                WD_FIND_ELEMENT_FUNC[selector_type])
        else:
            func_name = "find_element_by_{0}".format(
                WD_FIND_ELEMENT_FUNC[selector_type])

        return func_name

# end
