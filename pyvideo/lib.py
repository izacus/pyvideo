__author__ = 'Jernej Virag'

from ctypes import cdll, util

def load_avbin():
    """
    Loads avbin library and returns it
    """

    # TODO: Support Windows
    libname = util.find_library("avbin")
    lib = cdll.LoadLibrary(libname)
    return lib