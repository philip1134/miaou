# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


__version__ = "0.2.0"


from miaou.app import Application
from miaou.scanner.base import Scanner


def generate(**attrs):
    """main caller"""

    Application(**attrs).main()


# end
