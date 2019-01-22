from distutils.core import setup
from setuptools import find_packages
from setuptools.command.install import install
import os
import sys
import io
import versioneer

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="homematicip",
    packages=find_packages(exclude="tests"),
    long_description=long_description,
    description="An API for the homematicip cloud",
    author="Heimo Stieg",
    author_email="stieg@corona-bytes.net",
    url="https://github.com/coreGreenberet/homematicip-rest-api",
    download_url="https://github.com/coreGreenberet/homematicip-rest-api/tarball/"
    + versioneer.get_version(),
    keywords=["homematicip"],  # arbitrary keywords
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
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
    python_requires=">=3",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
