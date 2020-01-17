import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib
from setuptools.command.build_ext import build_ext


with open("README.md", "r") as f:
    long_description = f.read()

def patch_bin_path(cmd, conf):

    bin_name = conf.get('bin_name')

    if not os.path.isabs(bin_name):
        print('Patching "bin_name" to properly install_scripts dir')
        try:
            if not os.path.exists(cmd.install_scripts):
                os.makedirs(cmd.install_scripts)
            conf.set('bin_name',
                     os.path.join(cmd.install_scripts, conf.get('bin_name')))
        except Exception:
            conf.set('bin_name', sys.prefix + '/bin/' + bin_name)


setup(
    name="tinydns",
    packages=find_packages(),
    version = '0.0.1',
    description='this project is a tinydns automaton implementation by python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zhaoheng12/tinydns/',
    author='zhaohengping',
    author_email='zhaohengping@gongchang.com',
    data_files =['tinydns.conf'],
    package_dir = {'tinydns.conf':'etc'},
    install_requires = ["gevent","dnslib","redis"],
    entry_points = {
                  'console_scripts': [
                      'tinydns = tinydns.__init__:tinydns',
                  ],
              },
    package_data={
            '': ['*.rst'],
        }

)
