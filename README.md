# django-dsl

![Licence](https://img.shields.io/github/license/treussart/django-dsl.svg) ![Version](https://img.shields.io/github/tag/treussart/django-dsl.svg)

Provides a rich query language, which interprets a string into a Query.
This is a simple query language for Django ORM that allows you to search via wildcards and regexes by specifying the database column name.

You can give it to your customers so they will be able to filter the database without having to edit code.

## Usage

### Characters allowed:

* Key (column name) : `A-Za-z0-9_.`
* Value : all except : `)(` and white space.

### Query Parser Syntax:

* Wildcard Searches: *

  * *test : All that ends by test
  * test* : All that starts by test
  * \*test* : All that contains test
  * `\*test\*` : All equal to \*test\*
  * `\*test*` : All that starts by *test
  * `*test\*` : All that ends by test*
* [Regex](https://docs.python.org/3/library/re.html) Searches: ~
  * ~\W+ : Matches any non-word character.
  * `\~test` : Matches all equal to ~test.
* Boolean Operators: `AND` `OR` `NOT`
* Grouping: `( )`
* Date and number Searches (operators: `<` `>` `<=` `>`) :

  * key>2 : All greater than 2
  * key<=2 : All less than or equal to 2
  * key>2018-05-04 : All greater than 2018-05-04
  * key<=2018-05-04 : All less than or equal to 2018-05-04
* Date Range Searches (inclusive) (which correspond to SQL queries of BETWEEN):
  * key:2018-05-04_2018-05-05
* Null Searches (which correspond to SQL queries of IS NULL and IS NOT NULL):

  * key:True
  * key:False


## How to Use

### Requirements

- Python 3.9+

### Installing It

    pip install django-domain-specific-language

### Running It

Example in a database:

![DB image](https://raw.githubusercontent.com/treussart/django-dsl/master/example-db.png)


    class Table(models.Model):
        country = models.CharField(max_length=255)
        product = models.CharField(max_length=255)
        sales = models.IntegerField()


Example of possible expressions:

* `country:India AND Product:Ice-cream`
* `country:*a* AND NOT Product:~.*e$`

In case you get the expression in the URL parameters:

    def my_view(request):
        from django_dsl.run import compile_expr
        query = compile_expr(request.GET['expression'])
        elements = Table.objects.filter(query)

Now you're able to run and use the DSL!
