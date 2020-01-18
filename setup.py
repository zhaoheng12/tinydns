import shutil
from pkg_resources import Requirement, resource_filename
try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup,find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tinydns",
    packages=find_packages(),
    version='0.0.1',
    description='this project is a tinydns automaton implementation by python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zhaoheng12/tinydns/',
    author='zhaohengping',
    author_email='zhaohengping@gongchang.com',
    data_files = [('/etc', ['tinydns.conf'])],
    classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7.15",
      ],
    install_requires=["gevent","dnslib"],
    entry_points={
                  'console_scripts': [
                      'tinydns=tinydns.__init__:main',
                  ],
              },
    package_data={
            '': ['*.rst'],
        }

)

filename = resource_filename(Requirement.parse("tinydns"),"etc/tinydns.conf")
target = '/etc/tinydns.conf'
try:
   shutil.copyfile(filename, target)
except IOError as e:
   print("Unable to copy file. %s" % e)