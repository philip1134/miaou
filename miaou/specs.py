# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-26
#


import os
import time
import miaou.logger as logger
import miaou.utils as utils


class Specs:
    """api specs"""

    def __init__(self):
        """initializer"""

        self.apis = {}

# public
    def append(self, module, apis):
        """append api spec"""

        if module not in self.apis:
            self.apis[module] = []

        self.apis[module] += apis

    def print(self, output_path=".", combined=True):
        """print to yaml file"""

        if not os.path.exists(output_path):
            logger.error("the output path does not exsit.")
            return

        # make result folder
        result_path = os.path.join(
            output_path,
            "pyzentao_specs_%s" % time.strftime("%Y_%m_%d_%H_%M_%S")
        )

        os.makedirs(result_path)

        # print to file
        if combined:
            # print specs to one file
            self._print_to_file(
                path=os.path.join(result_path, "specs.yml"),
                specs=utils.flatten(self.apis.values())
            )
        else:
            # print specs by module
            for key, apis in self.apis.items():
                self._print_to_file(
                    path=os.path.join(
                        result_path, self._url_to_filename(key)),
                    specs=apis
                )

# private
    def _print_to_file(self, path, specs):
        """print spec to yaml file"""

        text = ""
        for spec in specs:
            text += "%s:\n" % spec["name"]
            text += "    method: %s\n" % spec["method"]
            text += "    path: %s\n" % spec["path"]
            if len(spec["params"]) > 0:
                text += "    params:\n"
                for param in spec["params"]:
                    text += "        - %s\n" % param
            text += "\n"

        logger.info("print to '%s'" % os.path.basename(path))
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(text)

    @classmethod
    def _url_to_filename(self, url):
        """convert url to spec file name"""

        filename = url.split("/")[-1]
        filename = filename.split("?")[0]
        filename = filename.split("-")[-1]
        filename = filename.split(".")[0]
        return "%s.yml" % filename

# end
