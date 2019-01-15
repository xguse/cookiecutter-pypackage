# -*- coding: utf-8 -*-
"""Provide functions specific to config files."""
from pathlib import Path

from logzero import logger as log
import yaml

from munch import Munch, munchify


def load_config(path):
    """Return fully instantiated config tree."""
    if path is None:
        log.info("returning empty config object.")
        return Munch()

    path = Path(path)
    config = yaml.safe_load(path.open())
    config = pathify_config(config)
    config = munchify(config)

    return config


def walk_config(config, test, action):
    """Walk config tree, performing `action(value)` on each config value where test(key, value) returns True."""
    for key, value in config.items():
        if isinstance(value, dict):
            walk_config(config=value, test=test, action=action)
        elif test(key, value):
            config[key] = action(value)
        else:
            pass


def pathify_config(config):
    """Return config after converting the values of keys that end in `_PATH` or `_DIR` to path objects."""

    def is_path(key, value):
        path_endings = ["PATH", "DIR"]
        key_ending = key.split("_")[-1]
        return key_ending in path_endings

    def pathify(path):
        if path is None:
            return None
        return Path(path)

    walk_config(config=config, test=is_path, action=pathify)

    return config
