from setuptools import setup, find_packages

__version__ = '1.0.1'

setup(
    name='maildocker',
    version=str(__version__),
    packages=find_packages(),
    description='Maildocker library for Python',
    long_description=open('./README.rst').read(),
    install_requires=['urllib2'],
)
