# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-03-01
#


class Scanner:
    """scanner base class"""

    def open(self, site_url, username, password):
        """tear up works"""

        pass

    def close(self):
        """tear down works"""

        pass

    def get_module_groups(self, dev_url):
        """get module group page urls

        return url string list [url]
        """

        pass

    def get_apis(self, api_url):
        """get apis from api page

        return list like [{name, method, path, params}]
        """

        pass

# end
