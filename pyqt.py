#!/usr/bin/env python

import argparse
import sys

from PyQt5.QtWidgets import QApplication

from utility.table.tabledialog import TableDialog

import idata.config


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=argparse.FileType("r", encoding="utf-8"))
    parser.add_argument("source")

    args = parser.parse_args(argv)

    config = idata.config.load_yaml(args.config)
    if isinstance(config, idata.config.csv.CSVTableSourceConfig):
        with open(args.source, encoding="cp932") as fp:
            source = config.load(fp)
    elif isinstance(config, idata.config.excel.ExcelTableSourceConfig):
        source = config.load(args.source)
    else:
        raise NotImplementedError

    app = QApplication(argv)

    win = TableDialog()
    win.setSource(source)
    win.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
