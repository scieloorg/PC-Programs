# code: utf-8

import json
import socket

try:
    import urllib.request as urllib_request
    from urllib.parse import urlencode as urllib_parse_urlencode
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.request import ProxyHandler, build_opener, install_opener
    from urllib.error import HTTPError, URLError
except ImportError:
    import urllib as urllib_request
    from urllib import urlencode as urllib_parse_urlencode
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError, URLError
    from urllib2 import ProxyHandler, build_opener, install_opener


from .. import encoding


def fix_ip(ip):
    if '://' in ip:
        ip = ip.split('://')[1]
    return ip


class ProxyInfo(object):

    def __init__(self, server=None, port=None, user=None, password=None):
        self.server = server
        self.port = port
        self.user = user
        self.password = password

    @property
    def handler_data(self):
        r = {}
        if self.server is not None and self.port is not None:
            proxy_handler_data = ''
            if self.user is not None and self.password is not None:
                proxy_handler_data = self.user + ':' + self.password + '@'
            proxy_handler_data += fix_ip(self.server) + ':' + self.port
            if len(proxy_handler_data) > 0:
                r = {'http': 'http://'+proxy_handler_data,
                     'https': 'https://'+proxy_handler_data}
        return r


def ask_data(server='', port=''):
    import ws_proxy_gui
    proxy_info = ws_proxy_gui.display_proxy_form(server, port)
    if proxy_info is not None:
        ip, port, user, password = proxy_info
        proxy_info = ProxyInfo(ip, port, user, password)
    return proxy_info


def registry_proxy_opener(proxy_handler_data):
    proxy_handler = ProxyHandler(proxy_handler_data)
    opener = build_opener(proxy_handler)
    install_opener(opener)
