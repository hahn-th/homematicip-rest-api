from distutils.core import setup
from setuptools import find_packages

VERSION = '0.7'

setup(
    name='homematicip',
    packages=find_packages(exclude='tests'),
    version=VERSION,
    description='An API for the homematicip cloud',
    author='Heimo Stieg',
    author_email='stieg@corona-bytes.net',
    url='https://github.com/coreGreenberet/homematicip-rest-api',
    download_url='https://github.com/coreGreenberet/homematicip-rest-api/tarball/' + VERSION,
    keywords=['homematicip'],  # arbitrary keywords
    classifiers=[],
    install_requires=["requests", "websocket-client", "future", "aiohttp"]
)
