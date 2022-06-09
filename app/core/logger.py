"""Logging python module."""
import os
import logging.config
import yaml

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, "log_config.yaml")

with open(filename, "r", encoding="UTF-8") as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)
