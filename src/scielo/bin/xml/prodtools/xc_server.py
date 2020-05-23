# coding=utf-8
import logging
import logging.config
import argparse

from prodtools import xc


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


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

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    collection_acron = args.collection_acron
    call_download = args.call_download
    call_gerapadrao = args.call_gerapadrao

    reception = xc.Reception(collection_acron)

    if call_download:
        reception.download_packages()

    reception.receive_package()

    if call_gerapadrao:
        reception.gerapadrao()
