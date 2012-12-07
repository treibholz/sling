#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import subprocess
import os
import time
#from pprint import pprint

history_file = os.path.expanduser("~/.sling_history")

class Executables(object): # {{{
    """docstring for Executables"""
    def __init__(self):
        super(Executables, self).__init__()

        paths = os.environ["PATH"].split(os.pathsep)
        self.data = {}

        for p in paths:
            for f in os.listdir(p):
                if self.is_exec(p, f):
                    try:
                        self.data[f].append(p)
                    except:
                        self.data[f] = [p]

    def is_exec(self, p, f):
        """docstring for is_exec"""
        file_path = os.path.join(p,f)
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    def get(self, query):
        """docstring for get"""
        if query in self.data.keys():
            print query

# }}}

###############################################################################

class History(object): # {{{
    """docstring for History"""
    def __init__(self):
        super(History, self).__init__()
        try:
            self.history = [c.split(';',2) for c in open(history_file).readlines()]
        except:
            self.history = []

        self.pos = len(self.history)


    def cursor(self, move):
        """docstring for cursor"""
        self.pos += move

        if self.pos <= 0:
            self.pos = len(self.history) - 1
        elif self.pos >= ( len(self.history) -1):
            self.pos = 0

        return self.history[self.pos]

# }}}

###############################################################################

class MyCommand(object): # {{{
    """docstring for MyCommand"""
    def __init__(self, command):
        super(MyCommand, self).__init__()
        self.command = command

        self.pid = False
        self.valid = True
        self.start_time = time.time()

    def store_history(self):
        """docstring for store_historyi"""
        history_entry = '%s;%s;%s\n' % (self.start_time, self.pid, self.command, )
        open(history_file,'a').write(history_entry)

    def run(self):
        """docstring for run"""
        self.pid = subprocess.Popen(self.command).pid
        self.store_history()

# }}}

###############################################################################

class CliWindow(Gtk.Window): # {{{

    def __init__(self):
        Gtk.Window.__init__(self, title="Sling")

        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        self.h      = History()
        self.e      = Executables()
        self.cli    = Gtk.Entry()

        self.cli.connect("activate", self.on_enter)
        self.cli.connect("key-release-event", self.on_key_press_event)

        self.add(self.cli)


    def on_enter(self, widget):
        c = MyCommand(widget.get_text())

        if c.valid:
            c.run()
            Gtk.main_quit()
        else:
            pass

    def on_key_press_event(self, widget, key):
        key_code = key.get_keycode()[1]
        if key_code == 111:
            widget.set_text(self.h.cursor(-1)[2].strip('\n'))

        elif key_code == 116:
            widget.set_text(self.h.cursor(1)[2].strip('\n'))

        else:
            self.e.get(widget.get_text())

# }}}

win = CliWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()




# vim:fdm=marker:ts=4:sw=4:sts=4:ai:sta:et
