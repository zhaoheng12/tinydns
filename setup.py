import os
from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

extras_require = {
    'backends': ['redis>=3.0.0'],
    'redis': ['redis>=3.0.0'],
}

setup(
    name='tinydns',
    version=__import__('tinydns').__version__,
    description='this project is a tinydns automaton implementation by python',
    long_description=long_description,
    author='zhaohengping',
    author_email='zhaohengping@gongchang.com',
    url='https://github.com/zhaoheng12/tinydns/',
    packages=find_packages(),
    extras_require=extras_require,
    package_data={
        'tinydns': [
        ],
    },

)
