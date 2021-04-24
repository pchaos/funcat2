#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from os.path import dirname, join
from setuptools import (
    find_packages,
    setup,
)

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


with open(join(dirname(__file__), 'funcat/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

try: 
    # AttributeError: 'ParsedRequirement' object has no attribute 'req'; for pip >=20.1
    req=[str(ir.requirement) for ir in parse_requirements("requirements.txt", session=False)],
except:
    req=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],

setup(
    name='funcat2',
    version=version,
    description='funcat2',
    packages=find_packages(exclude=[]),
    author='Hua Liang',
    url='https://github.com/pchaos/funcat2',
    author_email='et@everet.org',
    license='Apache License v2',
    package_data={'': ['*.*']},
    install_requires=req,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
