#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

with open('VERSION') as version_file:
    version = version_file.read()
    version = version.strip()

install_requirements = [
    'packtools',
    'pillow',
]

dependency_links = [
]

setup(
    name='xpm e xc',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requirements,
    dependency_links=dependency_links,
)
