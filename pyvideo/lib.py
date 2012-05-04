__author__ = 'Jernej Virag'

import os
from ctypes import cdll, util

def load_avbin():
    """
    Loads avbin library and returns it
    """

    if os.name == "nt":
        lib = cdll.LoadLibrary("avbin.dll")
    else:
		libname = util.find_library("avbin")
		lib = cdll.LoadLibrary(libname)
		
    return lib