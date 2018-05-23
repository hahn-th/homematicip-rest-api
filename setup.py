from distutils.core import setup
from setuptools import find_packages
from setuptools.command.install import install
import os
import sys
import io

VERSION = '0.9.4'
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format( tag, VERSION )
            sys.exit(info)

setup(
    name='homematicip',
    packages=find_packages(exclude='tests'),	
    long_description=long_description,
    version=VERSION,
    description='An API for the homematicip cloud',
    author='Heimo Stieg',
    author_email='stieg@corona-bytes.net',
    url='https://github.com/coreGreenberet/homematicip-rest-api',
    download_url='https://github.com/coreGreenberet/homematicip-rest-api/tarball/' + VERSION,
    keywords=['homematicip'],  # arbitrary keywords
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only'],
    install_requires=["requests>=2.4.3", "websocket-client", "websockets", "aiohttp", "async_timeout"],
    scripts=['hmip_cli.py', 'hmip_generate_auth_token.py'],
	python_requires='>=3',
	cmdclass={
        'verify': VerifyVersionCommand,
    }
)
