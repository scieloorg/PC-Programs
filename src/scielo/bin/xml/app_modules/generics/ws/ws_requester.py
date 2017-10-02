# code: utf-8

import json
import socket

try:
    import urllib.request as urllib_request
    from urllib.parse import urlencode as urllib_parse_urlencode
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
except ImportError:
    import urllib as urllib_request
    from urllib import urlencode as urllib_parse_urlencode

    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError, URLError

try:
    import tkinter as tk
except ImportError:
    try:
        import Tkinter as tk
    except:
        print('no Tkinter')

from .. import encoding


# JOURNALS_CSV_URL = 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'


def local_gettext(text):
    return text


try:
    from ...__init__ import _
except:
    _ = local_gettext


def get_servername(url):
    server = url
    server = server[server.find('://')+3:]
    if '/' in server:
        server = server[:server.find('/')]
    return server


def try_request(url, timeout=30, debug=False, force_error=False):
    response = None
    socket.setdefaulttimeout(timeout)
    req = Request(encoding.encode(url))
    http_error_proxy_auth = None
    error_message = ''
    try:
        response = urlopen(req, timeout=timeout).read()
        response = encoding.decode(response)
    except HTTPError as e:
        if e.code == 407:
            http_error_proxy_auth = e.code
        error_message = e.read()
    except URLError as e:
        if '10061' in str(e.reason):
            http_error_proxy_auth = e.reason
        error_message = 'URLError'
    except Exception as e:
        error_message = 'Unknown'
        try:
            error_message += ': ' + str(e)
        except Exception as e:
            pass
    if force_error is True:
        response = None
        http_error_proxy_auth = True
    if error_message != '':
        encoding.debugging(
            'ws_requester.try_request()',
            (url, error_message, response, http_error_proxy_auth))
    return (response, http_error_proxy_auth, error_message)


class WebServicesRequester(object):

    def __init__(self, active=True, proxy_info=None):
        self.requests = {}
        self.skip = []
        self.proxy_info = proxy_info
        if proxy_info is not None:
            server, port = proxy_info.split(':')
            self.proxy_info = ProxyInfo(server, port)
        self.active = active
        self.instance = None

    def format_url(self, url, parameters=None):
        #if isinstance(text, unicode):
        #    text = text.encode('utf-8')
        #values = {
        #            'q': text,
        #          }
        query = ''
        if parameters is not None:
            parameters = {name: encoding.encode(value) for name, value in parameters.items()}
            query = '?' + urllib_parse_urlencode(parameters)
        return url + query

    def request(self, url, timeout=30, debug=False, force_error=False):
        if self.active is False:
            return None
        response = self.requests.get(url)
        if response is None and url not in self.requests.keys():
            server = get_servername(url)
            if server not in self.skip:
                response, http_error_proxy_auth, error_message = try_request(url, timeout, debug, force_error)
                if http_error_proxy_auth is not None:
                    if self.proxy_info is not None:
                        get_proxy_info(self.proxy_info)
                        response, http_error_proxy_auth, error_message = try_request(url, timeout, debug, force_error)
                if response is None and error_message != '':
                    self.skip.append(server)
                self.requests[url] = response
        return response

    def json_result_request(self, url, timeout=30, debug=False):
        if self.active is False:
            return None
        result = None
        if url is not None:
            r = self.request(url, timeout, debug)
            if r is not None:
                result = json.loads(encoding.encode(r))
        return result

    def is_valid_url(self, url, timeout=30):
        if self.active is False:
            return None
        _result = self.request(url, timeout)
        return _result is not None


def get_proxy_info(proxy_data):
    from . import ws_proxy
    server, port = proxy_data.split(':')
    proxy_info = ws_proxy.ask_data(server, port)
    ws_proxy.registry_proxy_opener(proxy_info.handler_data)

