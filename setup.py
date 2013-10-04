# setup.py
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ex = [Extension("main", ["participant.pyx"])]

for e in ex:
		e.cython_directives = {"profile": True}


setup (
	cmdclass = {'build_ext': build_ext},
	ext_modules = ex
)

