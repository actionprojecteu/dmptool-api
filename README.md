# DMPTOOL-API


## What is it?

dmptool-api is the backend of the dmptool application, which it generate data managment plans for the ACTION projects.


## Files

The api files in order are:
 - [application/app.py](application/app.py) : controls the requests and responses of the server.
 - [application/config.py](application/config.py) : contains the differents configurations for the server.
 - [application/models.py](application/models.py) : contains the model for the tables of the sql database.
 - [application/resources.py](application/resources.py) : resources for the api (empty for the moment).
 - [db/dbase.db](db/dbase.dbd) : database sqlite3 for users and projects.
 - [manage.py](manage.py) : main python file with several command options for managing the database and start the server.
 - [Dockerfile](Dockerfile) : file for dockerize the api.
 - [requeriments.txt](requeriments.txt) : the libraries necessary for the proper functioning of the server.

## Manage.py