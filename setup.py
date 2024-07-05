#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='rest_framework_cart',
    version='0.1.0',
    url='https://github.com/alxkahovsky/',
    license='MIT',
    description='Shopping Cart for Django REST Framework',
    author='Alexey Yakovlev',
    author_email='yakovlevtech@yandex.ru',
    packages=get_packages('rest_framework_cart'),
    package_data=get_package_data('rest_framework_cart'),
    zip_safe=False,
    install_requires=[
        'djangorestframework',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
