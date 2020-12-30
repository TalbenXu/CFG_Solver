from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("CFGR.pyx"),
    ext_modules=cythonize("grammar.pyx"),
    ext_modules=cythonize("matrix.pyx"),
    ext_modules=cythonize("solver.pyx"),
)