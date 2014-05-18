#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "0.3.2"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='webhooks',
    version=version,
    description='Python + Webhooks mMade Easy',
    long_description=readme + '\n\n' + history,
    author='Daniel Greenfeld',
    author_email='pydanny@gmail.com',
    url='https://github.com/pydanny/webhooks',
    packages=[
        'webhooks',
        'webhooks.senders'
    ],
    package_dir={'webhooks':
                 'webhooks'},
    include_package_data=True,
    install_requires=[
        'wrapt',
        'requests>=2.2.1',
        'cached-property>=0.1.2'
    ],
    license="BSD",
    zip_safe=False,
    keywords='webhooks',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
