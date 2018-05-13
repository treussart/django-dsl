django-dsl
==========

|Licence| |Version|

+------------------+--------------------+
| Status           | Operating system   |
+==================+====================+
| |Build_Status|   | Linux x86\_64      |
+------------------+--------------------+

Requirements
------------

-  PLY
-  Django

Installation
------------

::

   pip install django-domain-specific-language

Usage
-----

Allows you to search by specifying the name of the column of the
database.

Characters allowed:

* Key (column name) : `A-Za-z0-9_.`
* Value : A-Za-z0-9_~*.^$?{}[]|!\/+-éèàû

Query Parser Syntax:

* Wildcard Searches: *

  * *\test : All that ends by test
  * test\* : All that starts by test
  * *\test\* : All that contains test
* `Regex`_ Searches: ~

  * ~\W+ : Matches any character which is not a word character.
* Boolean Operators: AND OR NOT
* Grouping: ( )

Example
-------

Your database:

.. figure:: https://raw.githubusercontent.com/treussart/django-dsl/master/example-db.png
   :alt: DB image

   DB image

The possible researches:

* Country:India AND Product:Ice-cream
* Country:\*a\* AND NOT Product:~.*e$

In your code:

::

   from django_dsl.run import compile
   result = compile(request.GET['expression'])

.. _Regex: https://docs.python.org/3/library/re.html

.. |Build_Status| image:: https://travis-ci.org/treussart/django-dsl.svg?branch=master
   :target: https://travis-ci.org/treussart/django-dsl

.. |Version| image:: https://img.shields.io/github/tag/treussart/django-dsl.svg
.. |Licence| image:: https://img.shields.io/github/license/treussart/django-dsl.svg
