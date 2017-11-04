from distutils.core import setup

setup(
    name='homematicip',
    packages=['homematicip', 'homematicip.async'],
    version='0.7',
    description='An API for the homematicip cloud',
    author='Heimo Stieg',
    author_email='stieg@corona-bytes.net',
    url='https://github.com/coreGreenberet/homematicip-rest-api',
    download_url='https://github.com/coreGreenberet/homematicip-rest-api/tarball/0.7',
    keywords=['homematicip'],  # arbitrary keywords
    classifiers=[],
    install_requires=["requests", "websocket-client", "future", 'aiohttp','async_timeout']
)
