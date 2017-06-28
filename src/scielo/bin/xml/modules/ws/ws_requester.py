# code: utf-8

import os
import json
import socket
import urllib2

try:
    import Tkinter
except:
    pass


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
JOURNALS_CSV_URL = 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'


def local_gettext(text):
    return text


try:
    from __init__ import _
except:
    _ = local_gettext


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


class ProxyGUI(object):

    def __init__(self, tkFrame, registered_ip, registered_port, debug=False):
        self.info = None
        self.debug = False

        if registered_ip is None:
            registered_ip = ''
        if registered_port is None:
            registered_port = ''

        self.tkFrame = tkFrame

        self.tkFrame.labelframe_window = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_window.pack(fill="both", expand="yes")

        self.tkFrame.labelframe_message = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_message.pack(fill="both", expand="yes")
        self.tkFrame.label_message = Tkinter.Label(self.tkFrame.labelframe_message, text=_('This tool requires Internet access for some services, such as DOI, affiliations, and other data validations, and also to get journals data from SciELO.\n\nIf you do not use a proxy to access the Internet, and click on Cancel button.'), font="Verdana 12 bold", wraplength=450)
        self.tkFrame.label_message.pack()

        self.tkFrame.labelframe_proxy_ip = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_proxy_ip.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_ip = Tkinter.Label(self.tkFrame.labelframe_proxy_ip, text='Proxy IP / server', font="Verdana 12 bold")
        self.tkFrame.label_proxy_ip.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_ip = Tkinter.Entry(self.tkFrame.labelframe_proxy_ip)
        self.tkFrame.entry_proxy_ip.insert(0, registered_ip)
        self.tkFrame.entry_proxy_ip.pack()

        self.tkFrame.labelframe_proxy_port = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=5)
        self.tkFrame.labelframe_proxy_port.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_port = Tkinter.Label(self.tkFrame.labelframe_proxy_port, text='Proxy Port', font="Verdana 12 bold")
        self.tkFrame.label_proxy_port.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_port = Tkinter.Entry(self.tkFrame.labelframe_proxy_port)
        self.tkFrame.entry_proxy_port.insert(0, registered_port)
        self.tkFrame.entry_proxy_port.pack()

        self.tkFrame.labelframe_proxy_user = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_user = Tkinter.Label(self.tkFrame.labelframe_proxy_user, text=_('user'), font="Verdana 12 bold")
        self.tkFrame.label_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_user = Tkinter.Entry(self.tkFrame.labelframe_proxy_user)
        self.tkFrame.entry_proxy_user.pack()

        self.tkFrame.labelframe_proxy_password = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_proxy_password.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_password = Tkinter.Label(self.tkFrame.labelframe_proxy_password, text=_('password'), font="Verdana 12 bold")
        self.tkFrame.label_proxy_password.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_password = Tkinter.Entry(self.tkFrame.labelframe_proxy_password, show='*')
        self.tkFrame.entry_proxy_password.pack()

        self.tkFrame.labelframe_buttons = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_buttons.pack(fill="both", expand="yes")

        self.tkFrame.button_cancel = Tkinter.Button(self.tkFrame.labelframe_buttons, text=_('Cancel'), command=lambda: self.tkFrame.quit())
        self.tkFrame.button_cancel.pack(side='right')

        self.tkFrame.button_execute = Tkinter.Button(self.tkFrame.labelframe_buttons, text=_('OK'), command=self.register)
        self.tkFrame.button_execute.pack(side='right')

    def register(self):
        r = [self.tkFrame.entry_proxy_ip.get(), self.tkFrame.entry_proxy_port.get(), self.tkFrame.entry_proxy_user.get(), self.tkFrame.entry_proxy_password.get()]
        self.info = [None if item == '' else item for item in r]
        self.tkFrame.quit()


def ask_data(server='', port=''):
    proxy_info = display_proxy_form(server, port)
    if proxy_info is not None:
        ip, port, user, password = proxy_info
        proxy_info = ProxyInfo(ip, port, user, password)
    return proxy_info


def display_proxy_form(registered_ip, registered_port, debug=False):
    tk_root = Tkinter.Tk()
    tk_root.title(_('Proxy information'))
    tkFrame = Tkinter.Frame(tk_root)

    main = ProxyGUI(tkFrame, registered_ip, registered_port, debug)
    main.tkFrame.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
    tk_root.focus_set()

    r = main.info
    main = None
    if debug:
        print('proxy informed:')
        print(r)
    tk_root.destroy()
    return r


def registry_proxy_opener(proxy_handler_data):
    proxy_handler = urllib2.ProxyHandler(proxy_handler_data)
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)


def try_request(url, timeout=30, debug=False, force_error=False):
    response = None
    socket.setdefaulttimeout(timeout)
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    req = urllib2.Request(url)
    http_error_proxy_auth = None
    error_message = ''
    try:
        response = urllib2.urlopen(req, timeout=timeout).read()
    except urllib2.HTTPError as e:
        if e.code == 407:
            http_error_proxy_auth = e.code
        error_message = e.read()
    except urllib2.URLError as e:
        if '10061' in str(e.reason):
            http_error_proxy_auth = e.reason
        error_message = 'URLError'
    except urllib2.socket.timeout:
        error_message = 'Time out!'
    except Exception as e:
        error_message = 'Unknown!'
        #raise
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
        self.active = active

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(WebServicesRequester, self).__new__(self)
        return self.instance

    def request(self, url, timeout=30, debug=False, force_error=False):
        #print(url)
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
                result = json.loads(r)
        return result

    def is_valid_url(self, url, timeout=30):
        if self.active is False:
            return None
        _result = self.request(url, timeout)
        return _result is not None
