from setuptools import setup, find_packages

try:
    from wheel.bdist_wheel import bdist_wheel
    HAS_WHEEL = True
except ImportError:
    HAS_WHEEL = False


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tinydns",
    packages=find_packages(),
    version = '0.0.2',
    description='this project is a tinydns automaton implementation by python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zhaoheng12/tinydns/',
    author='zhaohengping',
    author_email='zhaohengping@gongchang.com',
    package_data={
            '': ['*.rst'],
        }

)
