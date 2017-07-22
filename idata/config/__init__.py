# -*- coding: utf-8 -*-

import yaml

from . import csv
from .yaml_represent import *


def load_yaml(fp):
    data = yaml.load(fp)
    if data.get("mimeType") == "text/csv":
        return csv.CSVTableSourceConfig(**data)
    raise NotImplementedError


def save(data, fp):
    def _save(data, fp):
        kwargs = dict(allow_unicode=True, default_flow_style=False)
        return fp.write(yaml.dump(data, **kwargs))

    if isinstance(fp, str):
        with open(fp, "w", encoding="utf-8") as fp:
            return _save(data, fp)
    return _save(data, fp)
