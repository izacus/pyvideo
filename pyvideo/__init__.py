"""
This is an AVBin based video decoding package
"""
import avbin

__author__ = 'Jernej Virag'

def load(filename, skip_video=False):
    source = avbin.AVbinSource(filename, skip_video=skip_video)
    return source