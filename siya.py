#!/usr/bin/env python
import os
import signal
import gi
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

Gdk.threads_init()

SERVER_COMMAND = '/home/ays/alms/manage.py runserver'.split(" ")
LOG_FILE = open("serrverlog", "w+")
SERVER_PROCESS = None


def execute(command):
    stdout_lines = iter(SERVER_PROCESS.stdout.readline, "")
    for stdout_line in stdout_lines:
        print stdout_line
        yield stdout_line
    SERVER_PROCESS.stdout.close()
    returncode = SERVER_PROCESS.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, command)


def run(logViewerView):
    try:
        execute_gen = execute(SERVER_COMMAND)
    except subprocess.CalledProcessError:
        return False
    for x in execute_gen:
        print x
        buffer = logViewerView.get_buffer()
        text = buffer.get_text(
                buffer.get_start_iter(),
                buffer.get_end_iter(),
                False)
        buffer.set_text(text)
    return False


class Handler:
    def __init__(self, builder):
        self.builder = builder

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        SERVER_PROCESS.terminate()
        os.kill(SERVER_PROCESS.pid, signal.SIGINT)
        return False

    def onCloseMainWindow(self, *args):
        self.onDeleteWindow()

    def onStartServerButtonClicked(self, object):
        global SERVER_PROCESS
        global LOG_FILE
        SERVER_PROCESS = subprocess.Popen(SERVER_COMMAND,
                                          stdout=LOG_FILE,
                                          stderr=LOG_FILE)


builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(Handler(builder))

window = builder.get_object("mainWindow")

window.show_all()

Gtk.main()
