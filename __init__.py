"""
This is an AVBin based video decoding package
"""
import avbin

def load(filename):
    source = avbin.AVbinSource(filename)
    return source