"""
@package CompoundPye.src
This file initializes all sub-packages.

Usage examples will be added soon.
"""
from logging import config
from .logger_config import LOGGER_CONFIG_DICT
config.dictConfig(LOGGER_CONFIG_DICT)
