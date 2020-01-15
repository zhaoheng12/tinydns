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
    packages=find_packages(),
    version = '0.0.1',
    description='this project is a tinydns automaton implementation by python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zhaoheng12/tinydns/',
    author='zhaohengping',
    author_email='zhaohengping@gongchang.com',
    extras_require=extras_require,
package_data={
        '': ['*.rst'],
    }
)
