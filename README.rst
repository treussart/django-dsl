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
* Value : all except ')' '(' and white space. 

Query Parser Syntax:

* Wildcard Searches: *

  * *test : All that ends by test
  * test\* : All that starts by test
  * *test\* : All that contains test
  * \\*test\\* : All equal to \*test\*
  * \\*test* : All that starts by *test
  * \*test\\\* : All that ends by test*
* `Regex`_ Searches: ~

  * ~\W+ : Matches any character which is not a word character.
  * \\~test : Matches all equal to \~test.
* Boolean Operators: AND OR NOT
* Grouping: ( )
* Date and number Searches (operators: < > <= >=) :

  * key>2
  * key<=2
* Date Range Searches (inclusive) (which correspond to SQL queries of BETWEEN):

  * key:2018-05-04_2018-05-05
* Null Searches (which correspond to SQL queries of IS NULL and IS NOT NULL):

  * key:True
  * key:False

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
   query = compile(request.GET['expression'])
   cls.objects.filter(query)

.. _Regex: https://docs.python.org/3/library/re.html

.. |Build_Status| image:: https://travis-ci.org/treussart/django-dsl.svg?branch=master
   :target: https://travis-ci.org/treussart/django-dsl

.. |Version| image:: https://img.shields.io/github/tag/treussart/django-dsl.svg
.. |Licence| image:: https://img.shields.io/github/license/treussart/django-dsl.svg
