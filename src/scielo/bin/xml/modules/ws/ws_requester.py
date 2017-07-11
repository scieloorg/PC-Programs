# code: utf-8

import os
import json
import socket

try:
    import tkinter as tk
    import urllib.request as urllib_request
    import urllib.parse.urlencode as urllib_parse_urlencode
except ImportError:
    import Tkinter as tk
    import urllib as urllib_request
    from urllib import urlencode as urllib_parse_urlencode

from ..useful import utils
from ..useful import encoding


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
JOURNALS_CSV_URL = 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'


def local_gettext(text):
    return text


try:
    from ..__init__ import _
except:
    _ = local_gettext


def pathname2url(filename):
    return urllib_request.pathname2url(filename)


def fix_ip(ip):
    if '://' in ip:
        ip = ip.split('://')[1]
    return ip


def get_servername(url):
    server = url
    server = server[server.find('://')+3:]
    if '/' in server:
        server = server[:server.find('/')]
    return server


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


class ProxyGUI(tk.Frame):

    def __init__(self, tk_root, registered_ip, registered_port):
        self.info = None
        if registered_ip is None:
            registered_ip = ''
        if registered_port is None:
            registered_port = ''

        tk.Frame.__init__(self, tk_root)
        self.tk_root = tk_root
        self.tk_root.resizable(False, False)

        message_frame = tk.Frame(self)
        message_frame.pack(fill="both", expand="yes")
        message = tk.Message(message_frame,
            font='System 14 bold',
            text=_("""This tool requires Internet access for some services, 
                such as DOI, affiliations, and other data validations,
                and also to get journals data from SciELO.\n
                If you do not use a proxy to access the Internet,
                and click on Cancel button."""),
            wraplength=450
            )
        message.pack()

        proxy_ip_frame = tk.Frame(self)
        proxy_ip_frame.pack(fill="both", expand="yes")
        label_proxy_ip = tk.Label(proxy_ip_frame, text='Proxy IP / server')
        label_proxy_ip.pack(fill="both", expand="yes")
        self.proxy_ip_entry = tk.Entry(proxy_ip_frame)
        self.proxy_ip_entry.insert(0, registered_ip)
        self.proxy_ip_entry.pack()
        self.proxy_ip_entry.focus_set()

        proxy_port_frame = tk.Frame(self)
        proxy_port_frame.pack(fill="both", expand="yes")
        proxy_port_label = tk.Label(proxy_port_frame, text='Proxy Port')
        proxy_port_label.pack(fill="both", expand="yes")
        self.proxy_port_entry = tk.Entry(proxy_port_frame)
        self.proxy_port_entry.insert(0, registered_port)
        self.proxy_port_entry.pack()

        proxy_user_frame = tk.Frame(self)
        proxy_user_frame.pack(fill="both", expand="yes")
        proxy_user_label = tk.Label(proxy_user_frame, text=_('user'))
        proxy_user_label.pack(fill="both", expand="yes")
        self.proxy_user_entry = tk.Entry(proxy_user_frame)
        self.proxy_user_entry.pack()

        proxy_pass_frame = tk.Frame(self)
        proxy_pass_frame.pack(fill="both", expand="yes")
        proxy_pass_label = tk.Label(proxy_pass_frame, text=_('password'))
        proxy_pass_label.pack(fill="both", expand="yes")
        self.proxy_pass_entry = tk.Entry(proxy_pass_frame, show='*')
        self.proxy_pass_entry.pack()

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill="both", expand="yes")

        cancel_button = tk.Button(buttons_frame, text=_('Cancel'), command=lambda: self.tk_root.quit())
        cancel_button.pack(side='right')

        execute_button = tk.Button(buttons_frame, text=_('OK'), command=self.register)
        execute_button.pack(side='right')

    def register(self):
        r = [self.proxy_ip_entry.get(), self.proxy_port_entry.get(), self.proxy_user_entry.get(), self.proxy_pass_entry.get()]
        self.info = [None if item == '' else item for item in r]
        self.tk_root.quit()


def ask_data(server='', port=''):
    proxy_info = display_proxy_form(server, port)
    if proxy_info is not None:
        ip, port, user, password = proxy_info
        proxy_info = ProxyInfo(ip, port, user, password)
    return proxy_info


def display_proxy_form(registered_ip, registered_port, debug=False):
    tk_root = tk.Tk()
    tk_root.title(_('Proxy information'))

    app = ProxyGUI(tk_root, registered_ip, registered_port, debug)
    app.pack(side="top", fill="both", expand=True)

    app.mainloop()
    app.focus_set()

    r = app.info
    if debug:
        print('proxy informed:')
        print(r)
    tk_root.destroy()
    return r


def registry_proxy_opener(proxy_handler_data):
    proxy_handler = urllib_request.ProxyHandler(proxy_handler_data)
    opener = urllib_request.build_opener(proxy_handler)
    urllib_request.install_opener(opener)


def try_request(url, timeout=30, debug=False, force_error=False):
    response = None
    socket.setdefaulttimeout(timeout)
    req = urllib_request.Request(utils.uni2notuni(url))
    http_error_proxy_auth = None
    error_message = ''
    try:
        response = urllib_request.urlopen(req, timeout=timeout).read()
        response = utils.notuni2uni(response)
    except urllib_request.HTTPError as e:
        if e.code == 407:
            http_error_proxy_auth = e.code
        error_message = e.read()
    except urllib_request.URLError as e:
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
        print((url, error_message, response, http_error_proxy_auth))
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

    def __new__(self, active, proxy_info):
        if not hasattr(self, 'instance'):
            self.instance = super(WebServicesRequester, self).__new__(self, active, proxy_info)
        return self.instance

    def format_url(self, url, parameters=None):
        #if isinstance(text, unicode):
        #    text = text.encode('utf-8')
        #values = {
        #            'q': text,
        #          }
        query = ''
        if parameters is not None:
            parameters = {name: encoding.uni2notuni(value) for name, value in parameters.items()}
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
                        server, port = self.proxy_info.split(':')
                        proxy_info = ask_data(server, port)
                        registry_proxy_opener(proxy_info.handler_data)
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
                result = json.loads(encoding.uni2notuni(r))
        return result

    def is_valid_url(self, url, timeout=30):
        if self.active is False:
            return None
        _result = self.request(url, timeout)
        return _result is not None
