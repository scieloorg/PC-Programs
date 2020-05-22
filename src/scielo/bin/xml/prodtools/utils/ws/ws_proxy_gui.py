try:
    import tkinter as tk
except ImportError:
    try:
        import Tkinter as tk
    except:
        print('no Tkinter')

from prodtools.utils import encoding


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


def display_proxy_form(registered_ip, registered_port, debug=False):
    tk_root = tk.Tk()
    tk_root.title(_('Proxy information'))

    app = ProxyGUI(tk_root, registered_ip, registered_port, debug)
    app.pack(side="top", fill="both", expand=True)

    app.mainloop()
    app.focus_set()

    r = app.info
    if debug:
        encoding.debugging('display_proxy_form()', r)
    tk_root.destroy()
    return r
