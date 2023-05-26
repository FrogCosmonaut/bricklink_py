from setuptools import setup, find_packages

from bricklink_py import version

setup(
   name='bricklink_py',
   version=version,
   description='Python wrapper of the bricklink API v3',
   author='Juan Franco',
   author_email='github@juanfg.es',
   packages=find_packages(),
   install_requires=[],
)