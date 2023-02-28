# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-26
#


import click


def info(message):
    """print normal message in stdout."""

    click.echo(message)


def stage(message):
    """print stage message in stdout."""

    click.secho(message, fg="green")


def warning(message):
    """print warning message in stdout."""

    click.secho("[WARNING] " + message, fg="yellow")


def error(message):
    """print error message in stdout."""

    click.secho("[ERROR] " + message, fg="red")


# end
