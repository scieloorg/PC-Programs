#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
from setuptools import setup
import setuptools
import codecs
import sys


if sys.version_info[0:2] < (3, 5):
    raise RuntimeError('Requires Python 3.5 or newer')

with codecs.open('README.md', mode='r', encoding='utf-8') as fp:
    README = fp.read()


INSTALL_REQUIRES = [
    'packtools>=2.6.4',
    'Pillow>=6.2.2,<8.4.0',
]


EXTRAS_REQUIRE = {
}


TESTS_REQUIRE = [
]


if int(setuptools.__version__.split('.', 1)[0]) < 18:
    assert "bdist_wheel" not in sys.argv, "setuptools 18 required for wheels."
    if sys.version_info[0:2] < (3, 5):
        INSTALL_REQUIRES.append('pathlib>=1.0.1')
else:
    EXTRAS_REQUIRE[':python_version<"3.5"'] = ['pathlib>=1.0.1']

if sys.version_info[0:2] == (2, 7):
    TESTS_REQUIRE.append('mock')

setup(
    name="SciELO Production Tools",
    version="1.0",
    description="Produces XML packages and databases to publish",
    long_description=README,
    long_description_content_type="text/markdown",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    maintainer="SciELO Devs",
    maintainer_email="scielo-dev@googlegroups.com",
    license="BSD License",
    url="http://docs.scielo.org",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "docs",
                 "app_data", "modules",
                 "modules.*", "modules.*.*",
                 ]
    ),
    package_data={
        'prodtools': ['locale/*/LC_MESSAGES/*.mo',
                      'settings/*/*.txt',
                      'settings/*/*.csv',
                      'settings/*/*.fst',
                      'settings/*/*.ini',
                      ],
        '': ['*.xsl', '*.dtd', '.ent', '*.ini', '*.xml', '*.mod', '*.txt'],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: XML Producers and SciELO Collection Managers",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tests_require=TESTS_REQUIRE,
    test_suite='tests',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts":[
            "scieloxpm=prodtools.xpm:main",
            "scielojournals=prodtools.download_markup_journals:main",
            "scielo2pubmed=prodtools.xml_pubmed:main",
            "scieloxc=prodtools.xc:main",
            "scieloxcserver=prodtools.xc_server:main",
            "xml_transform=prodtools.xml_transform:main",
        ]
    }
)
