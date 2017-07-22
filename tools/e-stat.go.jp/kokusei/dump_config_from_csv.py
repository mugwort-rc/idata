#!/usr/bin/env python3

import argparse
import os
import sys
from collections import OrderedDict
import csv
import re
import hashlib

import yaml

sys.path.append(".")

import idata.config
import idata.config.excel
from idata.config.yaml_represent import *


def calc_sha1(filename):
    with open(filename, "rb") as fp:
        return hashlib.sha1(fp.read()).hexdigest()


def cast_int_list(v):
    try:
        return [int(v)]
    except:
        return list(map(int, v.split(",")))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r", encoding="cp932"))
    parser.add_argument("quantitative_column_start")
    parser.add_argument("name_index")
    parser.add_argument("--bigtitle", default=0, type=int)
    parser.add_argument("--title", default=1, type=int)
    parser.add_argument("--alias-index", default=None)
    parser.add_argument("--start-index", default=None, type=int)
    parser.add_argument("--type", default="")
    parser.add_argument("--unit", default="")

    args = parser.parse_args()

    name_index = cast_int_list(args.name_index)
    alias_index = cast_int_list(args.alias_index)
    if isinstance(alias_index, list):
        start_index = args.start_index or alias_index[-1] + 1
    else:
        start_index = args.start_index or alias_index + 1

    if isinstance(args.quantitative_column_start, str):
        args.quantitative_column_start = idata.config.excel.name_to_col(args.quantitative_column_start)

    config = OrderedDict([
        ("survey", OrderedDict([
            ("country", "jp"),
            ("name", "国勢調査"),
            ("datetime", "2015-10-01T00:00:00+0900"),
        ])),
        ("title", ""),
        ("title:en", ""),
        ("creator", OrderedDict([
            ("name", "総務省統計局"),
            ("homepage", "http://www.stat.go.jp/"),
        ])),
        ("source", [OrderedDict([
            ("url", "http://www.stat.go.jp/data/kokusei/2015/"),
            ("last_visit", "2017-07-20"),
        ])]),
        ("notes", []),
        ("type", "simpleTable"),
        ("mimeType", "text/csv"),
        ("hints", [OrderedDict([
            ("type", "filename"),
            ("regex", os.path.basename(args.input.name)),
        ]), OrderedDict([
            ("type", "digest"),
            ("data", ["sha1:{}".format(calc_sha1(args.input.name))]),
        ])]),
        ("startIndex", start_index),
        ("columns", []),
        ("asserts", OrderedDict([
            ("prepare", []),
        ])),
    ])

    names_rows = []
    aliases_rows = []
    for i, row in enumerate(csv.reader(args.input)):
        if i == args.bigtitle:
            config["asserts"]["prepare"].append(OrderedDict([
                ("type", "row"),
                ("row", i),
                ("f", "eq"),
                ("args", OrderedDict([
                    ("source", 1),
                    ("value", row[1]),
                ])),
            ]))
        elif i == args.title:
            title = row[args.quantitative_column_start]
            m = re.search("第[^表]+表", title)
            config["asserts"]["prepare"].append(OrderedDict([
                ("type", "row"),
                ("row", i),
                ("f", "in"),
                ("args", OrderedDict([
                    ("value", m.group()),
                    ("source", args.quantitative_column_start),
                ])),
            ]))
            config["title"] = title
        elif i == args.title + 1:
            title = row[args.quantitative_column_start]
            config["title:en"] = title
        elif i in name_index:
            names = row[args.quantitative_column_start:]
            if len(name_index) == 1:
                value = "$config@columns[{}:]@name".format(args.quantitative_column_start-1)
            else:
                value = "$config@columns[{}:]@names[{}]".format(args.quantitative_column_start-1, len(names_rows))
            names_rows.append(names)
            config["asserts"]["prepare"].append(OrderedDict([
                ("type", "row"),
                ("row", i),
                ("f", "eq"),
                ("args", OrderedDict([
                    ("source", "{}:_1+{}".format(args.quantitative_column_start, len(names))),
                    ("value", value),
                ])),
            ]))
        elif i in alias_index:
            aliases_rows.append(row[args.quantitative_column_start:])
        if i > start_index:
            break

    names = map(list, zip(*names_rows))
    aliases = map(list, zip(*aliases_rows))
    for name, alias in zip(names, aliases):
        d = OrderedDict([
            ("name", ",".join(name)),
            ("names", name),
            ("aliases", [" - ".join(alias)]),
            ("type", args.type),
            ("dataType", "quantitative"),
            ("unit", args.unit),
        ])
        if len(name) == 1:
            del d["names"]
        config["columns"].append(d)

    idata.config.save(config, sys.stdout)

    return 0


if __name__ == "__main__":
    sys.exit(main())
