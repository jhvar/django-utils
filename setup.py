#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: jhvar
# Mail: jhvar@outlook.com
# Created Time:  2020-8-11 15:42:43
#############################################


from setuptools import setup, find_packages

# with open("README.md", "r", encoding='utf-8') as fh:
#     long_description = fh.read()

long_description = '''

django-role-router is a simply, definition designed router with multi-roles.

You can install it with pip. >pip install django-role-router

To use it, make sure you have installed django-role-router already.

1. Insert middleware jhvar.django.urls.middleware.JvRoleMiddleware after SessionMiddleware.

2. You can define app role permission like "permitted_roles = ['admin']" in urls.py global section.

3. You can define path role permission like "jv_path('admin', views.my_admin, name='my_admin', roles=['admin'])" in urlpatterns list. Path role has more priority than app role.

4. We have supported regex format with "jv_re_path" function, just like "jv_path". It can also work with rest_framework router.

5. You can define logger 'jhvar.django.logger' in urls.py logger section, to print debug info.

Now, you have role permission verifier, you should add your role granty in somewhere.

It just like "grant_roles(request, 'admin')" or "grant_roles(request, ('admin', 'super'))" or  "grant_roles(request, ['admin', 'super'])". 


Join it, have fun!


Visit https://github.com/jhvar/django-utils for more detail.

'''

setup(
    name = "django-role-router",
    version = "0.2.1",
    keywords = ("pip", "django", "role", "util"),
    description = "Make django router with role permission",
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