#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-keyed-urls',
    version=__import__('keyed_urls').__version__,
    description='So simple you\'ll burst into tears right away.',
    long_description=read('README.rst'),
    author='Matthias Kestenholz',
    author_email='mk@406.ch',
    url='http://github.com/matthiask/django-keyed-urls/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'django-modeltranslation',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    zip_safe=False,
)
