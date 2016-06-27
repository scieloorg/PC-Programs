# code: utf-8

import socket
import urllib2

import Tkinter


def local_gettext(text):
    return text


try:
    from __init__ import _
except:
    _ = local_gettext


class ProxyGUI(object):

    def __init__(self, tkFrame, debug=False):
        self.info = None
        self.debug = False

        self.tkFrame = tkFrame

        self.tkFrame.labelframe_window = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_window.pack(fill="both", expand="yes")

        self.tkFrame.labelframe_message = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_message.pack(fill="both", expand="yes")
        self.tkFrame.label_message = Tkinter.Label(self.tkFrame.labelframe_message, text=_('This tool requires Internet access to validate DOI, affiliations, and other data, and also to get journals data from SciELO. Inform the required data, if applies.'), font="Verdana 12 bold")
        self.tkFrame.labelframe_proxy_ip = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_proxy_ip.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_ip = Tkinter.Label(self.tkFrame.labelframe_proxy_ip, text='Proxy IP', font="Verdana 12 bold")
        self.tkFrame.label_proxy_ip.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_ip = Tkinter.Entry(self.tkFrame.labelframe_proxy_ip)
        self.tkFrame.entry_proxy_ip.pack()

        self.tkFrame.labelframe_proxy_port = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_proxy_port.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_port = Tkinter.Label(self.tkFrame.labelframe_proxy_port, text='Proxy Port', font="Verdana 12 bold")
        self.tkFrame.label_proxy_port.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_port = Tkinter.Entry(self.tkFrame.labelframe_proxy_port)
        self.tkFrame.entry_proxy_port.pack()

        self.tkFrame.labelframe_proxy_user = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_user = Tkinter.Label(self.tkFrame.labelframe_proxy_user, text=_('user'), font="Verdana 12 bold")
        self.tkFrame.label_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_user = Tkinter.Entry(self.tkFrame.labelframe_proxy_user)
        self.tkFrame.entry_proxy_user.pack()

        self.tkFrame.labelframe_proxy_password = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
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


def ask_proxy_info(debug=False):
    tk_root = Tkinter.Tk()
    tk_root.title(_('Proxy information'))
    tkFrame = Tkinter.Frame(tk_root)
    main = ProxyGUI(tkFrame, debug)
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
        proxy_info += proxy_server + ':' + proxy_port

    if len(proxy_info) > 0:
        proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy_info, 'https': 'https://'+proxy_info})
    else:
        proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)


def try_request(url, timeout=30, debug=False, force_error=False):
    response = None
    socket.setdefaulttimeout(timeout)
    req = urllib2.Request(url)
    error_code = None
    error_message = ''
    try:
        response = urllib2.urlopen(req).read()
    except urllib2.HTTPError as e:
        error_code = e.code
        error_message = e.read()
    except urllib2.URLError as e:
        error_message = 'URLError'
    except urllib2.socket.timeout:
        error_message = 'Time out!'
    except Exception as e:
        error_message = 'Unknown!'
        raise
    if force_error is True:
        response = None
        error_code = True
    return (response, error_code, error_message)


def depricated_request(url, timeout=30, debug=False, force_error=False):
    response, error_code, error_message = try_request(url, timeout, debug, force_error)
    if response is None:
        if error_code is not None:
            if debug:
                print('Try with proxy no authenticated')
            registry_proxy()
            response, error_code, error_message = try_request(url, timeout, debug, force_error)
    if response is None:
        if error_message == 'URLError':
            if debug:
                print('Try with proxy authenticated: ask proxy info')
            proxy_info = ask_proxy_info(debug)
            if debug:
                print(proxy_info)
            if proxy_info is not None:
                ip, port, user, password = proxy_info
                registry_proxy(ip, port, user, password)
                if debug:
                    print('Try with proxy authenticated: execute')
                response, error_code, error_message = try_request(url, timeout)
    if response is None:
        print(_('Unable to access'))
        print(url)
        print(error_message)

    return response


def use_authenticated_proxy():
    proxy_info = ask_proxy_info()
    if proxy_info is not None:
        ip, port, user, password = proxy_info
        registry_proxy(ip, port, user, password)


def request(url, timeout=30, debug=False, force_error=False):
    response, error_code, error_message = try_request(url, timeout, debug, force_error)
    if response is None and error_code is not None:
        use_authenticated_proxy()
        response, error_code, error_message = try_request(url, timeout, debug, force_error)
    return response
