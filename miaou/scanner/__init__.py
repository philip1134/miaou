# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


from miaou.scanner.selenium_scanner import SeleniumScanner


class Scanner:
    """scanner factory"""

    _map = {
        "selenium": SeleniumScanner,
    }

    @classmethod
    def get(cls, scanner):
        """get scanner by scanner type"""

        if isinstance(scanner, str):
            return cls._map.get(scanner, SeleniumScanner)()
        else:
            # maybe customized scanner
            return scanner

# end
