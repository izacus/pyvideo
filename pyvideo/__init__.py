"""
This is an AVBin based video decoding package
"""
import avbin

__author__ = 'Jernej Virag'

def load(filename, skip_video=False, keyframes_only=False):
    source = avbin.AVbinSource(filename, skip_video=skip_video, keyframes_only=keyframes_only)
    return source
