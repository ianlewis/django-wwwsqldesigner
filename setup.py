#!/usr/bin/env python

from setuptools import setup, find_packages
 
setup (
    name='django-wwwsqldesigner',
    version='0.1',
    description='A django backend for wwwsqldesigner',
    author='Ian Lewis',
    author_email='IanMLewis@gmail.com',
    url='http://www.bitbucket.org/IanLewis/django-wwwsqldesigner/',
    license='MIT License',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
)
