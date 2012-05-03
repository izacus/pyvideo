__author__ = 'Jernej Virag'

class MediaException(Exception):
    pass

class MediaFormatException(MediaException):
    pass

class ImageException(MediaException):
    pass
