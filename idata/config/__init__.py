# -*- coding: utf-8 -*-

import yaml

from . import csv
from . import excel
from .yaml_represent import *


def load_yaml(fp):
    if isinstance(fp, str):
        fp = open(fp)
    data = yaml.load(fp)
    if data.get("mimeType") == "text/csv":
        return csv.CSVTableSourceConfig(**data)
    elif data.get("mimeType") == "application/vnd.ms-excel":
        return excel.ExcelTableSourceConfig(**data)
    raise NotImplementedError


def save(data, fp):
    def _save(data, fp):
        kwargs = dict(allow_unicode=True, default_flow_style=False)
        return fp.write(yaml.dump(data, **kwargs))

    if isinstance(fp, str):
        with open(fp, "w", encoding="utf-8") as fp:
            return _save(data, fp)
    return _save(data, fp)
