"""
This is an AVBin based video decoding package
"""
import avbin

__author__ = 'Jernej Virag'

def load(filename):
    source = avbin.AVbinSource(filename)
    return source