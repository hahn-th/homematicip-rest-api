from distutils.core import setup
from setuptools import find_packages

VERSION = '0.9.1'

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
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only'],
    install_requires=["requests", "websocket-client", "future", "websockets", "aiohttp"],
    scripts=['hmip_cli.py', 'hmip_generate_auth_token.py']
)
