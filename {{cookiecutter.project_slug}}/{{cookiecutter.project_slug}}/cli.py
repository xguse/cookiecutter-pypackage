# -*- coding: utf-8 -*-

"""Console script for {{cookiecutter.project_slug}}."""
from pathlib import Path
from pprint import pprint

import click

from logzero import logger as log
from munch import Munch

import {{cookiecutter.project_slug}}.api.commands as cmd

from . import configs

THIS_FILE = Path(__file__)


@click.group()
@click.option(
    "--config", "-c", help="Path to a configuration file.", type=click.Path(), default=None
)
@click.option("--show-config", help="Do nothing but print the configuration tree.", is_flag=True)
@click.pass_context
def main(ctx, config, show_config):
    """Console script for {{cookiecutter.project_slug}}."""
    ctx.ensure_object(dict)

    if config is not None:
        ctx.obj["CONFIG_PATH"] = Path(config)
        ctx.obj["CONFIG"] = configs.load_config(config)
    else:
        ctx.obj["CONFIG_PATH"] = None
        ctx.obj["CONFIG"] = None

    if show_config:
        pprint(ctx.obj["CONFIG"])
        exit(0)


if __name__ == "__main__":
    main()
