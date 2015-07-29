.. image:: https://travis-ci.org/python-dirbtuves/website.svg
   :target: https://travis-ci.org/python-dirbtuves/website

.. image:: https://coveralls.io/repos/python-dirbtuves/website/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/python-dirbtuves/website?branch=master 

pylab.lt website
================

Website for Python workshops internal needs.


Contacts
========

| Website: pylab.lt_
| Mailing list: https://groups.google.com/d/forum/python-dirbtuves

.. _pylab.lt: http://pylab.lt


Development environment
=======================

You need to create database manually::

  $ createdb pylab
  $ make
  $ bin/django migrate
  $ make testall
  $ make run
