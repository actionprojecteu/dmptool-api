# DMPTOOL-API


## What is it?

dmptool-api is the backend of the dmptool application, which it generate data managment plans for the [ACTION](https://actionproject.eu/) projects.


## Files

The api files in order are:
 - application:
 	- [app.py](application/app.py) : controls the requests and responses of the server.
 	- [config.py](application/config.py) : contains the differents configurations for the server.
 	- [models.py](application/models.py) : contains the model for the tables of the sql database.
 	- [resources.py](application/resources.py) : resources for the api (empty for the moment).
 - db:
 	- [dbase.db](db/dbase.dbd) : database sqlite3 for users and projects.
 - [manage.py](manage.py) : main python file with several command options for managing the database and start the server.
 - [Dockerfile](Dockerfile) : file for dockerize the api.
 - [requeriments.txt](requeriments.txt) : the libraries necessary for the proper functioning of the server.

### Manage.py

manage.py is the main python file of the api and it is used by command line. The possibles commands are:
- Manage tables: manage the tables of the sql database.
 	- Create tables: create the tables of the sql database.
```
python manage.py create_tables
```

 	- Delete tables: delete all the tables of the sql database (**Deletes all data**).
```
python manage.py drop_tables
```

 - Manage users: manage the user of the sql database.
 	- Create a normal user: username, password and email is required (promt input).
```
python manage.py create_user
```

 	- Create an admin user: username, password and email is required (promt input).
```
python manage.py create_admin
```

 	- Delete an user: username is required (promt input).
```
python manage.py delete_user
```

 - Manage projects: manage the projects of the sql database.
 	- Create a project: project and description is required (promt input).
```
python manage.py create_user
```

 	- Delete a project: project is required (promt input).
```
python manage.py delete_user
```

 - Manage user-project relationship: manage the relaion many-to-many between users and projects of the sql database.
 	- Create an user-project relationship: username and project name is required (promt input).
```
python manage.py create_relation
```

 	- Delete an user-project relationship: project is required (promt input).
```
python manage.py delete_relation
```




