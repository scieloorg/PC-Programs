# code: utf-8

import os
import json
import socket
import urllib2
from datetime import datetime

try:
    import Tkinter
except:
    pass

import fs_utils


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


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


class ProxyGUI(object):

    def __init__(self, tkFrame, registered_ip, registered_port, debug=False):
        self.info = None
        self.debug = False

        self.tkFrame = tkFrame

        self.tkFrame.labelframe_window = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_window.pack(fill="both", expand="yes")

        self.tkFrame.labelframe_message = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=50)
        self.tkFrame.labelframe_message.pack(fill="both", expand="yes")
        self.tkFrame.label_message = Tkinter.Label(self.tkFrame.labelframe_message, text=_('This tool requires Internet access for some services, such as DOI, affiliations, and other data validations, and also to get journals data from SciELO.\n\nIf you do not use a proxy to access the Internet, and click on Cancel button.'), font="Verdana 12 bold")
        self.tkFrame.label_message.pack()

        self.tkFrame.labelframe_proxy_ip = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=50)
        self.tkFrame.labelframe_proxy_ip.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_ip = Tkinter.Label(self.tkFrame.labelframe_proxy_ip, text='Proxy IP', font="Verdana 12 bold")
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

        self.tkFrame.labelframe_proxy_user = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=50)
        self.tkFrame.labelframe_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_user = Tkinter.Label(self.tkFrame.labelframe_proxy_user, text=_('user'), font="Verdana 12 bold")
        self.tkFrame.label_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_user = Tkinter.Entry(self.tkFrame.labelframe_proxy_user)
        self.tkFrame.entry_proxy_user.pack()

        self.tkFrame.labelframe_proxy_password = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=50)
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


def ask_proxy_info(registered_ip, registered_port, debug=False):
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


def registry_proxy(proxy_server=None, proxy_port=None, proxy_user=None, proxy_password=None):
    proxy_info = ''
    if proxy_user is not None and proxy_password is not None:
        proxy_info = proxy_user + ':' + proxy_password + '@'

    if proxy_server is not None and proxy_port is not None:
        proxy_info += fix_ip(proxy_server) + ':' + proxy_port

    if len(proxy_info) > 0:
        proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy_info, 'https': 'https://'+proxy_info})
    else:
        proxy_handler = urllib2.ProxyHandler({})
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
        raise
    if force_error is True:
        response = None
        http_error_proxy_auth = True
    if error_message != '':
        print((url, error_message, response, http_error_proxy_auth))
    return (response, http_error_proxy_auth, error_message)


class WebServicesRequester(object):

    def __init__(self):
        self.requests = {}
        self.registered_ip = ''
        self.registered_port = ''
        self.USE_PROXY = None
        self.proxy_info = None
        self.read_proxy_server_data()
        self.skip = []

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(WebServicesRequester, self).__new__(self)
        return self.instance

    def read_proxy_server_data(self):
        if os.path.isfile(CURRENT_PATH + '/proxy.info'):
            content = open(CURRENT_PATH + '/proxy.info').read()
            if ',' in content:
                self.registered_ip, self.registered_port = content.split(',')

    def update(self, ip, port):
        if ip != self.registered_ip or port != self.registered_port:
            self.registered_ip = ip
            self.registered_port = port
            open(CURRENT_PATH + '/proxy.info', 'w').write(ip + ',' + port)

    def request(self, url, timeout=30, debug=False, force_error=False):
        response = self.requests.get(url)
        if response is None and not url in self.requests.keys():
            server = get_servername(url)
            if not server in self.skip:
                response, http_error_proxy_auth, error_message = try_request(url, timeout, debug, force_error)
                if response is None and error_message != '':
                    self.skip.append(server)
                if response is None and http_error_proxy_auth is not None and self.USE_PROXY in [True, None]:
                    self.proxy_info = ask_proxy_info(self.registered_ip, self.registered_port)
                    if self.proxy_info is None:
                        self.USE_PROXY = False
                    else:
                        ip, port, user, password = self.proxy_info
                        registry_proxy(ip, port, user, password)
                        self.update(ip, port)
                        response, http_error_proxy_auth, error_message = try_request(url, timeout, debug, force_error)
                self.requests[url] = response

        return response

    def json_result_request(self, url, timeout=30, debug=False):
        result = None
        if url is not None:
            r = self.request(url, timeout, debug)
            if r is not None:
                result = json.loads(r)
        return result

    def is_valid_url(self, url, timeout=30):
        _result = self.request(url, timeout)
        return _result is not None


class PublishingWebServicesRequester(WebServicesRequester):

    def __init__(self):
        WebServicesRequester.__init__(self)
        self.journals_url = 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'
        self.journals_file_content = ''

    def journal_doi_prefix_url(self, issn, year=None):
        if year is None:
            year = datetime.now().year
        if issn is not None:
            return 'http://api.crossref.org/works?filter=issn:{issn},from-pub-date:{year}'.format(issn=issn, year=year)

    def article_doi_checker_url(self, doi):
        #PID|oldpid
        url = None
        if doi is not None:
            if 'doi.org' in doi:
                doi = doi[doi.find('doi.org/')+len('doi.org/'):]
            url = 'http://api.crossref.org/works/' + doi.strip()
        return url

    def update_journals_file(self):
        self.journals_file_content = self.request(self.journals_url)
        fs_utils.update_file_content_if_there_is_new_items(self.journals_file_content, self.downloaded_journals_filename)

    @property
    def downloaded_journals_filename(self):
        downloaded_filename = CURRENT_PATH + '/../../markup/downloaded_markup_journals.csv'
        if not os.path.isdir(CURRENT_PATH + '/../../markup'):
            os.makedirs(CURRENT_PATH + '/../../markup')
        return downloaded_filename


wsr = PublishingWebServicesRequester()
