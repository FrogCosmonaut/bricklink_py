from setuptools import setup, find_packages

from bricklink_py import __version__, __description__, __author__, __email__

setup(
   name='bricklink_py',
   version=__version__,
   description=__description__,
   author=__author__,
   author_email=__email__,
   packages=find_packages(),
   install_requires=["requests_oauthlib"],
)