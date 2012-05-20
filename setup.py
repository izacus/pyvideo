#!/usr/bin/env python

from distutils.core import setup
from Cython.Distutils import build_ext
from Cython.Distutils.extension import Extension

ext_modules = [Extension("avbin", ["avbin.pyx"], libraries=["avbin"])]

setup(name="PyVideo",
      version="0.1",
      description="Python video decoding library based on AVBin",
      author="Jernej Virag",
      author_email="jernej@virag.si",
      packages=["pyvideo"],
      cmdclass = { 'build_ext': build_ext },
      ext_modules = ext_modules
     )
