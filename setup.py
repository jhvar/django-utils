#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: jhvar
# Mail: jhvar@outlook.com
# Created Time:  2020-8-11 15:42:43
#############################################


from setuptools import setup, find_packages

setup(
    name = "django-utils",
    version = "0.1.0",
    keywords = ("pip", "django", "role", "util"),
    description = "A toolkit for django-2.2.5 or higher",
    long_description = "dynamic router controller with permited roles",
    license = "MIT Licence",

    url = "https://github.com/jhvar/django-utils",
    author = "jhvar",
    author_email = "jhvar@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        'python_version>=3.6.9',
        'django>=2.2.5'
    ]
)