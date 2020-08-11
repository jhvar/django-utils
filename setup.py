#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: jhvar
# Mail: jhvar@outlook.com
# Created Time:  2020-8-11 15:42:43
#############################################


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "jhvar-django-utils",
    version = "0.1.1",
    keywords = ("pip", "django", "role", "util"),
    description = "A toolkit for django-2.2.5 or higher",
    long_description = long_description,
    license = "MIT Licence",

    url = "https://github.com/jhvar/django-utils",
    author = "jhvar",
    author_email = "jhvar@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'django>=2.2.5'
    ],
    python_requires='>=3.6',
)