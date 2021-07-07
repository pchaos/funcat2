#!/bin/sh

# Generate pypi wheels universal package and upload

# 以下方式不支持markdown格式说明上传。
# python setup.py bdist_wheel --universal upload -r pypitest
# python setup.py bdist_wheel --universal upload -r pypi

# 以下方式支持markdown格式说明上传。
python setup.py sdist
python setup.py bdist_wheel

twine upload --repository funcat2 dist/funcat2-*-py3-none-any.whl -r pypi  --verbose

rm -rf build
