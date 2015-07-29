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


Project structure
=================

Principles
----------

We use `Separation of concerns`_, `Command-query separation`_ and `Multilayered
architecture`_ principles to organize code structure.

**Separation of concerns**

This is principle, when code is organized into modules by business logic.
Sometimes people name their modules something like ``utils`` or ``helpers``.
These names should be avoided, unless they live in a small scoped Django app,
for example ``accounts.utils`` or ``accounts/helpers`` would be good naming.

In other words, *SoC* principle tells us to separate our code by business logic,
not by code type or something like that.

**Command-query separation**

This principle tells us to separate commands and queries to separate modules.
In our case we separate commands and queries to single module called
``services``.

It means, that our ``models.py`` should be used only for model definitions, no
more logic should be put into ``models.py``, unless this is directly related
with model itself.

All business logic should go to ``services``. For Django apps with larger
scope, ``services`` should be a package with modules in it, for apps with
smaller scope, ``services`` can be a module.

**Multilayered architecture**

This principle explains, that it is not enough to have code organized by
business logic, we also need need layered architecture to be able to manage
dependencies between those modules more flexibly.

In Django case, we have these layers:

1. *Data access layer* - basically this is model definitions in ``models.py``.

2. *Business layer* - services, helpers, forms, utilities and so on.

3. *Application layer* - views, admin, sometimes helpers and forms.

4. *Presentation layer* - urls, templates.

*Multilayered architecture* have one important rule: *each layer can access
only same or lower layer*.


Structure
---------

At the top level project has these folders:

- *config* - contains project build configuration.

- *pylab* - this is the whole source code of our project.

- *scripts* - various utility scripts.

- *var* - files that are created or generated automatically, these files should
  not be kept under version control.

- *parts* - this is similar to *var* but used by Buildout_, usually we store
  static assets automatically downloaded by `hexagonit.recipe.download recipe`_
  or other artifacts created by other Buildout_ recipes.

Dependencies between apps
-------------------------

As mentioned above, *pylab* folder contains the source code and it contains
list of Django apps. Only ``locale`` ad ``settings`` are not apps. ``locale``
contains translation strings and ``settings`` - Django settings.

Also there is two special apps, ``core`` and ``website``.

Usually most of the code can be easily refactored when project grows, but
Django models are not that easy to refactor. Each refactoring that touches
models required database migrations and database migrations are something that
you have to be careful with.

To avoid refactoring issues, we keep all project data access logic in single
Django app called ``core``. Also this helps us to better manage dependencies
between apps. Since ``core`` contains data access logic which is lowest layer
according to *multilayered architecture*, this means, that is is very likely,
that most of the code will depend on this app. So since ``core`` tend to be
referenced by many other modules and apps, we keep ``core`` lean.

``website`` app is another special case and it belongs to *application* and
*presentation* layers. This means that no other apps can ``website`` depend on
``website``, but ``website`` should depend on all other apps. In other words,
``website`` works like top level app with purpose to connect all components in
order to assemble whole project.

The visualisation of app interdependencies could looks like this::

  +------------+
  | website    |
  +------------+
        |
        v   ,------+
  +------------+   |
  | other apps |<--+
  +------------+
        |
        v
  +------------+
  | core       |
  +------------+


.. _Multilayered architecture: https://en.wikipedia.org/wiki/Multilayered_architecture
.. _Separation of concerns: https://en.wikipedia.org/wiki/Separation_of_concerns
.. _Command-query separation: https://en.wikipedia.org/wiki/Command%E2%80%93query_separation
.. _Buildout: http://www.buildout.org/
.. _hexagonit.recipe.download recipe: https://pypi.python.org/pypi/hexagonit.recipe.download
