Compilación de ejecutables
================================================================

Mac OS X
----------------------------------------------------------------

Para hacer el ejecutable en Mac OS X Yosemite se utilizó [Py2App](https://pythonhosted.org/py2app/):


```
$ sudo easy_install -U py2app
$ py2applet --make-setup PeopleCounter.py
$ rm -rf build dist
$ python setup.py py2app -i requests --iconfile Icon-72.icns
```

Windows
----------------------------------------------------------------

Para hacer el ejecutable en Windows 7 se utilizó [PyInstaller](https://github.com/pyinstaller/pyinstaller):

* Descargar e instalar [Python 2.7.x](https://www.python.org/downloads/).
* Reiniciar la computadora (importante).
* Ejecutar en CMD: 

```> pip install pyinstaller```

* Descargar e instalar [pywin32](http://sourceforge.net/projects/pywin32/files/pywin32/Build216/pywin32-216.win32-py2.7.exe/download)(Solo con esta versión funciona).
* Reiniciar la computadora (importante).
* Ejecutar en CMD: 

```
> pyinstaller PeopleCounter.py -w -F --icon=Icon-72.ico
```

Linux
----------------------------------------------------------------

Para hacer el ejecutable en Ubuntu 14.04 se utilizó [PyInstaller](https://github.com/pyinstaller/pyinstaller):

```
$ sudo apt-get install python-pip
$ sudo apt-get install python-tk
$ sudo pip install pyinstaller
$ sudo pip install requests
$ pyinstaller PeopleCounter.py --onefile --noconfirm
```
