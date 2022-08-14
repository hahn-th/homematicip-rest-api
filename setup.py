import io
import os
from setuptools import find_packages
from setuptools.command.install import install
from distutils.core import setup
import versioneer

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="homematicip",
    packages=find_packages(exclude="tests"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="An API for the homematicip cloud",
    author="Thomas Hahn",
    author_email="post@thomas-hahn.org",
    url="https://github.com/hahn-th/homematicip-rest-api",
    download_url="https://github.com/hahn-th/homematicip-rest-api/tarball/"
    + versioneer.get_version(),
    keywords=["homematicip"],  # arbitrary keywords
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "requests>=2.24.0",
        "websocket-client>=1.0.0",
        "websockets>=8.1",
        "aiohttp>=3.6.2",
        "async_timeout>=3.0.1",
        "aenum>=2.2.4",
    ],
    package_data={"homematicip_demo": ["json_data/*.json"],},  # Optional
    scripts=["hmip_cli.py", "hmip_generate_auth_token.py"],
    python_requires="~=3.8",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
