import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='slack2sheet',
    version='',
    packages=find_packages(),
    install_requires=required,
    url='',
    license='',
    author='',
    author_email='',
    description=''
)
