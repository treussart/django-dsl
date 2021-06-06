# django-dsl

![Licence](https://img.shields.io/github/license/treussart/django-dsl.svg) ![Version](https://img.shields.io/github/tag/treussart/django-dsl.svg)

## Requirements

-  PLY
-  Django

## Installation

    pip install django-domain-specific-language

## Usage

Allows you to search by specifying the name of the column of the
database.

Characters allowed:

* Key (column name) : `A-Za-z0-9_.`
* Value : all except ')' '(' and white space.

Query Parser Syntax:

* Wildcard Searches: *

  * *test : All that ends by test
  * test* : All that starts by test
  * \*test* : All that contains test
  * `\*test\*` : All equal to \*test\*
  * `\*test*` : All that starts by *test
  * `*test\*` : All that ends by test*
* [Regex](https://docs.python.org/3/library/re.html) Searches: ~

  * ~\W+ : Matches any character which is not a word character.
  * \\~test : Matches all equal to \~test.
* Boolean Operators: AND OR NOT
* Grouping: ( )
* Date and number Searches (operators: < > <= >=) :

  * key>2 : All greater than 2
  * key<=2 : All less than or equal to 2
  * key>2018-05-04 : All greater than 2018-05-04
  * key<=2018-05-04 : All less than or equal to 2018-05-04
* Date Range Searches (inclusive) (which correspond to SQL queries of BETWEEN):

  * key:2018-05-04_2018-05-05
* Null Searches (which correspond to SQL queries of IS NULL and IS NOT NULL):

  * key:True
  * key:False

## Example

Your database:

![DB image](https://raw.githubusercontent.com/treussart/django-dsl/master/example-db.png)

The possible researches:

* Country:India AND Product:Ice-cream
* Country:\*a\* AND NOT Product:~.*e$

In your code:

    from django_dsl.run import compile_expr
    query = compile_expr(request.GET['expression'])
    cls.objects.filter(query)