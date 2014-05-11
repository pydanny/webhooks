#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='webhooks',
    version='0.1.0',
    description='Python + Webhooks mMade Easy',
    long_description=readme + '\n\n' + history,
    author='Daniel Greenfeld',
    author_email='pydanny@gmail.com',
    url='https://github.com/pydanny/webhooks',
    packages=[
        'webhooks',
    ],
    package_dir={'webhooks':
                 'webhooks'},
    include_package_data=True,
    install_requires=[
        'wrapt',
        'requests>=2.2.1',
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
    ],
    test_suite='tests',
)