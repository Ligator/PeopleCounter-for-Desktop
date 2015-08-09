#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contador de Personas (Versión de escritorio).
# Abel Augusto Pacheco Angeles
# Agosto de 2015
# Python 2.7.8

# Para hacer el ejecutable en Mac OS X se utilizó Py2App (https://pythonhosted.org/py2app/):
# $ sudo easy_install -U py2app
# $ py2applet --make-setup PeopleCounter.py
# $ rm -rf build dist
# $ python setup.py py2app -i requests --iconfile Icon-72.icns

# Para hacer el ejecutable en Windows 7 se utilizó PyInstaller (https://github.com/pyinstaller/pyinstaller):
# Descargar e instalar Python 2.7.x (https://www.python.org/downloads/)
# Reiniciar la computadora (importante)
# Ejecutar en CMD: > pip install pyinstaller
# Descargar e instalar pywin32 (Solo con esta versión funciona: http://sourceforge.net/projects/pywin32/files/pywin32/Build216/pywin32-216.win32-py2.7.exe/download)
# Reiniciar la computadora (importante)
# Ejecutar en CMD: > pyinstaller PeopleCounter.py -w -F --icon=Icon-72.ico

# Para hacer el ejecutable en Ubuntu 14.04 se utilizó PyInstaller (https://github.com/pyinstaller/pyinstaller):
# $ sudo apt-get install python-pip
# $ sudo apt-get install python-tk
# $ sudo pip install pyinstaller
# $ sudo pip install requests
# $ pyinstaller PeopleCounter.py --onefile --noconfirm

from Tkinter import *
import Tkinter
import requests # sudo easy_install requests
from threading import Timer
from time import sleep
import json

# http://stackoverflow.com/a/13151299/2621484
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

# http://stackoverflow.com/a/7966437/2621484
class ScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='400x200+0+0'
        master.geometry("{0}x{1}+0+0".format("750", "400"))

def call_venues():
    global rt
    global old_response
    global decoded
    rt.stop()
    if stopped == 0:
        response = requests.get(url=venues_address)
        print response.status_code
        if response.status_code == 200:
            labelStatusText.set("http://flextronicschallenge.herokuapp.com - Respuesta satisfactoria de la API")
            if old_response != response.text:
                old_response = response.text
                decoded = json.loads(response.text)
                print 'DECODED:', decoded
                Lb1.delete(0, END)
                var_name.set(decoded[selected]["name"])
                var_number.set(decoded[selected]["counter"])
                for x in decoded:
                    Lb1.insert(END, x["name"])

                Lb1.selection_set(selected)
            rt.start()
        else:
            labelStatusText.set("http://flextronicschallenge.herokuapp.com - ERROR: Error de conexión con la API")


def on_closing():
    print "Cerrando"
    global rt
    global stopped
    rt.stop()
    stopped = 1
    master.destroy()

def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)
    global selected
    selected = index
    var_name.set(decoded[index]["name"])
    var_number.set(decoded[index]["counter"])

# GLOBALS VARS ****************************************************************
venues_address = "http://flextronicschallenge.herokuapp.com/venues.json"
# venues_address = "http://localhost:3000/venues.json"
master = Tk()
var_number = StringVar()
var_name   = StringVar()
selected = 0
old_response = ""
stopped = 0
decoded = []
rt = RepeatedTimer(1, call_venues) # it auto-starts, no need of rt.start()


# MAIN PROGRAM ****************************************************************

master.tk.call('encoding', 'system', 'utf-8')
reload(sys)
sys.setdefaultencoding("utf-8")
master.title("Contador de personas")

frameBody      = Frame(master, bd=2, relief=SUNKEN)
frameLeftSide  = Frame(frameBody, bd=2, relief=SUNKEN)
frameRightSide = Frame(frameBody, bd=2, relief=SUNKEN)
frameStatusBar = Frame(master, bd=2, relief=RIDGE)

Lb1 = Listbox(frameLeftSide, width=30)
label_number = Label( frameRightSide, textvariable=var_number, relief=RAISED, font=("Helvetica", 200) )
label_name   = Label( frameRightSide, textvariable=var_name, relief=RAISED, font=("Helvetica", 50), height=3, wraplength=600 )

Lb1.bind('<<ListboxSelect>>', onselect)
Lb1.insert(1, "Descargando lista de lugares...")

label_number.pack(fill="both", expand=True)
label_name.pack(fill="both", expand=True)
Lb1.pack(side=TOP, fill="both", expand=True)
frameLeftSide.pack(side=LEFT, fill=Y)
frameRightSide.pack(side=RIGHT, fill="both", expand=True)
frameBody.pack(fill="both", expand=True)

labelStatusText = StringVar()
labelStatusText.set("Conectando a la API http://flextronicschallenge.herokuapp.com/")
labelStatus = Label(frameStatusBar, textvariable=labelStatusText)
labelStatus.pack(fill=X)
frameStatusBar.pack(fill=X)

app=ScreenApp(master)
master.protocol("WM_DELETE_WINDOW", on_closing)
master.mainloop()
