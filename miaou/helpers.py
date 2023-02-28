# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-07-18
#


import os
import re
import yaml


def print_result(result):
    """print result to yaml file"""

    text = ""
    for k, v in result.items():
        text += "%s:\n" % k
        text += "    method: %s\n" % v["method"]
        text += "    path: %s\n" % v["path"]
        if len(v["params"]) > 0:
            text += "    params:\n"
            for param in v["params"]:
                text += "        - %s\n" % param
        text += "\n"

    with open("results/apis.yml", mode="w", encoding="utf-8") as f:
        f.write(text)


def parse_text(text):
    """parse url text"""

    stage("parsing '%s'" % text)

    path = []
    params = []

    # remove namespace and suffix
    slices = re.split("\s+", text)
    method = slices[0].strip().upper()
    if "GET/POST" == method:
        method = "POST"

    url = slices[1].strip()
    for pattern in (
        r"^/zentao/",
        r"\.json.*$",
    ):
        url = re.sub(pattern, "", url)
        # url = url.replace(repl, "")

    # split path
    for t in url.split("-"):
        t = t.strip()
        if re.match("\[\w+\]", t) is None:
            info("- get path '%s'" % t)
            path.append(t)
        else:
            t = t.replace(r"[", "")
            t = t.replace(r"]", "")
            info("- get param '%s'" % t)
            params.append(t)

    return (method, "-".join(path), params)


def login(selenium, url, username, password):
    """login zentao"""

    selenium.driver.get(url)
    account = selenium.wait_for_element("input#account")
    account.send_keys(username)
    passwd = selenium.wait_for_element("input[name=password]")
    passwd.send_keys(password)
    auth = selenium.wait_for_element("button#submit")
    # auth.send_keys(Keys.ENTER)
    auth.click()


def load_path(path):
    """load spec from the specified path"""

    if os.path.isdir(path):
        # path is a directory

        specs = {}
        for file_name in os.listdir(path):
            specs.update(load_file(os.path.join(path, file_name)))

        return specs
    else:
        # path is a file
        return load_file(path)


def load_file(path):
    """load spec from the specified file path"""

    specs = {}

    if os.path.exists(path) and path.endswith(".yml"):
        with open(path, mode="r", encoding="utf-8") as f:
            specs.update(yaml.full_load(f.read()))

    return specs


def switch_to_content_iframe(selenium):
    """check out the iframe exists and switch into it"""

    try:
        ifr = selenium.wait_for_element(
            "iframe#appIframe-admin, iframe#appIframe-my")
        selenium.driver.switch_to.frame(ifr)
    except Exception:
        pass

# end
