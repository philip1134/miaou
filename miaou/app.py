# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-26
#


import urllib
import miaou.logger as logger
from miaou.scanner import Scanner
from miaou.specs import Specs


class Application:
    """main application functions"""

    def __init__(
        self,
        site_url,
        username,
        password,
        combined_print=True,
        scanner="selenium",
        dev_url=None,
    ):
        """initializer"""
        self.site_url = site_url
        self.dev_url = dev_url
        self.username = username
        self.password = password
        self.combined_print = combined_print

        if dev_url is None:
            self.dev_url = urllib.parse.urljoin(
                self.site_url, "zentao/dev-api-index.html")
        else:
            self.dev_url = dev_url

        self.scanner = Scanner.get(scanner)
        self.specs = Specs()

# public
    def main(self):
        """main routine"""

        # login
        self.scanner.open(
            site_url=self.site_url,
            username=self.username,
            password=self.password
        )

        # get module groups
        logger.stage("get module groups from '%s'..." % self.dev_url)
        modules = self.scanner.get_module_groups(self.dev_url)

        # get apis
        logger.stage("get apis...")
        for module_url in modules:
            self.specs.append(
                module=module_url,
                apis=self.scanner.get_apis(module_url)
            )

        # print out
        logger.stage("print specs...")
        self.specs.print(
            output_path=".",
            combined=self.combined_print,
        )

        self.scanner.close()

# end
