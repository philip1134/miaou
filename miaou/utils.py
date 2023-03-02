# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


def flatten(l):
    """make list flatten"""

    for _ in l:
        if isinstance(_, list):
            yield from flatten(_)
        else:
            yield _


# end
