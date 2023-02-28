# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


import re
import miaou.logger as logger


def flatten(l):
    """make list flatten"""

    for _ in l:
        if isinstance(_, list):
            yield from flatten(_)
        else:
            yield _


def parse_url_to_api_items(url):
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
            logger.info("- get path '%s'" % t)
            path.append(t)
        else:
            t = t.replace(r"[", "")
            t = t.replace(r"]", "")
            logger.info("- get param '%s'" % t)
            params.append(t)

    return (method, "-".join(path), params)
# end
