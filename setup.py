from distutils.core import setup

setup(name='asmsactivate',
    version='1.0',
    description='Async API wrapper for sms-activate',
    install_requires=["aiohttp","certifi"],
    author='optinsoft',
    author_email='optinsoft@gmail.com',
    keywords=['sms-activate','sms','async'],
    url='https://github.com/optinsoft/asmsactivate',
    packages=['asmsactivate']
)