# coding=utf-8
from __future__ import print_function, unicode_literals
import os
import argparse
import logging
from logging.config import dictConfig

from prodtools.utils.logging import LOGGING_CONFIG


dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(
        description='Caller cli utility')
    parser.add_argument(
        "app_name",
        help="app name")
    parser.add_argument(
        "start_path",
        help="start path")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    app_name = args.app_name
    start_path = args.start_path
    _start_path = os.getcwd()
    print(_start_path)
    print(start_path)
    os.system("cd {};{}".format(start_path, app_name))


if __name__ == '__main__':
    main()
