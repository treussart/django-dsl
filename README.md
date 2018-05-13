# django-dsl

## Requirements
- PLY
- Django

## Usage

Allows you to search by specifying the name of the column of the database.

Example:
In your DB : 
![DB image](https://raw.githubusercontent.com/treussart/django-dsl/master/example-db.png)


In your code :
```
from django_dsl.run import compile
result = compile(request.GET['expression'])
```
