# Copyright 2020 (Fairy)Phy

from distutils.core import setup
import py2exe

option = {
	"excludes": ["tkinter", "_posixshmem", "readline", "resource", "win32evtlog", "win32evtlogutil"],
	"optimize": 2,
	"compressed": True
}

setup(name="Python Calculator", version="0.2", options={"py2exe": option}, console=["main.py"], zipfile="python.lib")
