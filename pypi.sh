#!/bin/sh
#
# Generate pypi wheels universal package and upload
#
# python setup.py bdist_wheel --universal upload -r pypitest
python setup.py bdist_wheel --universal upload -r pypi
rm -rf build