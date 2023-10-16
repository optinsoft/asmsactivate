from distutils.core import setup
import re

s = open('asmsactivate/version.py').read()
v = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", s, re.M).group(1)

setup(name='asmsactivate',
    version=v,
    description='Async API wrapper for sms-activate',
    install_requires=["aiohttp","certifi"],
    author='optinsoft',
    author_email='optinsoft@gmail.com',
    keywords=['sms-activate','sms','async'],
    url='https://github.com/optinsoft/asmsactivate',
    packages=['asmsactivate']
)
