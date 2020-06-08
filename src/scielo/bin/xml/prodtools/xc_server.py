# coding=utf-8
import logging
import logging.config
import argparse

from prodtools import xc
from prodtools.utils.logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(
        description='XML Converter for Server cli utility')
    parser.add_argument(
        "collection_acron",
        help="collection acron which names the configuration file")
    parser.add_argument('--download', action='store_true',
                        help='download packages')
    parser.add_argument('--gerapadrao', action='store_true',
                        help='call gerapadrao')
    parser.add_argument('--loglevel', default='WARNING')
    args = parser.parse_args()

    logger.setLevel(args.loglevel.upper())

    collection_acron = args.collection_acron
    call_download = args.download
    call_gerapadrao = args.gerapadrao

    reception = xc.Reception(collection_acron)

    if call_download:
        reception.download_packages()

    reception.receive_package()

    if call_gerapadrao:
        reception.gerapadrao()


if __name__ == "__main__":
    main()
