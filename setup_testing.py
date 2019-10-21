from distutils.core import setup
from setuptools import find_packages
from setuptools.command.install import install
import os
import sys
import io
import versioneer
import configparser

here = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(here, "setup.cfg"))
config["versioneer"]["style"] = "pep440-pre"

with open(os.path.join(here, "setup.cfg"), "w") as configfile:
    config.write(configfile)

setup(
    name="homematicip-testing",
    packages=find_packages(exclude="tests"),
    long_description="This API will be build with the latest commit on the master branch automatically. Don't use it for productive environments.",
    description="An API for the homematicip cloud. NOT FOR PRODUCTION",
    author="Heimo Stieg",
    author_email="stieg@corona-bytes.net",
    url="https://github.com/coreGreenberet/homematicip-rest-api",
    download_url="https://github.com/coreGreenberet/homematicip-rest-api/tarball/"
    + versioneer.get_version(),
    keywords=["homematicip"],  # arbitrary keywords
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "requests>=2.4.3",
        "websocket-client>=0.54.0",
        "websockets",
        "aiohttp>3",
        "async_timeout",
        "aenum",
    ],
    scripts=["hmip_cli.py", "hmip_generate_auth_token.py"],
    python_requires="~=3.6",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
