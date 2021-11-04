import pybind11
from distutils.core import setup, Extension

ext_modules = [
    Extension(
        'cpp_text_check',
        ['library.cpp', 'compile_lib.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++11'],
    ),
]

setup(
    name='library',
    version='0.0.1',
    author='SokoMix',
    author_email='None',
    description='C++ lib for project',
    ext_modules=ext_modules,
    requires=['pybind11']
)