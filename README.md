# django-dsl

## Requirements
- PLY
- Django

## Usage

Allows you to search by specifying the name of the column of the database.

Characters allowed:
- Key (column name) : A-Za-z0-9\_\.
- Value : A-Za-z0-9\_\~\*\.\^\$\?\{\}\[\]\|\!\\\/\+\-éèàû

Query Parser Syntax:
- Wildcard Searches: *
  - *test : All that ends by test
  - test* : All that starts by test
  - *test\* : All that contains test
- [Regex](https://docs.python.org/3/library/re.html) Searches: ~ 
  - ~\W+ : Matches any character which is not a word character.
- Boolean Operators: AND OR NOT
- Grouping: ( )

## Example

Your database:

![DB image](https://raw.githubusercontent.com/treussart/django-dsl/master/example-db.png)

The possible researches:
- Country:India AND Product:Ice-cream
- Country:\*a* AND NOT Product:~.*e$


In your code:
```
from django_dsl.run import compile
result = compile(request.GET['expression'])
```
