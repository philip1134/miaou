# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


from miaou.scanner.selenium_scanner import SeleniumScanner
from miaou.scanner.api_scanner import ApiScanner


class ScannerFactory:
    """scanner factory"""

    _map = {
        "selenium": SeleniumScanner,
        "api": ApiScanner,
    }

    @classmethod
    def get(cls, scanner, config={}):
        """get scanner by scanner type"""

        if isinstance(scanner, str):
            return cls._map.get(scanner, SeleniumScanner)(config)
        else:
            # maybe customized scanner
            return scanner

# end
