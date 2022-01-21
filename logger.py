"""Logging python module."""

import logging.config
import yaml

with open("log_config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
