# DMPTOOL-API


## What is it?

dmptool-api is the backend of the [dmptool application](https://github.com/actionprojecteu/dmptool), which it generate data managment plans for the [ACTION](https://actionproject.eu/) projects.


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

[manage.py](manage.py) is the main python file of the api and it is used by command line. The possibles functions are:
 - **Manage tables**: manage the tables of the sql database.
 	- Create tables: create the tables of the sql database.
<br/>`python manage.py create_tables`
 	- Delete tables: delete all the tables of the sql database (**Deletes all data**).
<br/>`python manage.py drop_tables`
 - **Manage users**: manage the user of the sql database.
 	- Create a normal user: username, password and email is required (promt input).
<br/>`python manage.py create_user`
 	- Create an admin user: username, password and email is required (promt input).
<br/>`python manage.py create_admin`
 	- Delete a user: username is required (promt input).
<br/>`python manage.py delete_user`
 - **Manage projects**: manage the projects of the sql database.
 	- Create a project: project and description is required (promt input).
<br/>`python manage.py create_user`
 	- Delete a project: project is required (promt input).
<br/>`python manage.py delete_user`
 - **Manage user-project relationship**: manage the relaion many-to-many between users and projects of the sql database.
 	- Create a user-project relationship: username and project name is required (promt input).
<br/>`python manage.py create_relation`
 	- Delete a user-project relationship: project is required (promt input).
<br/>`python manage.py delete_relation`
 - **Start server**: start the python server from app.py.
 	- Development mode: start the development server. Optionals parameters: host (-h, --host), port (-p, --port).
<br/>`python manage.py runserver`
 	- Production mode: start the production server. Optionals parameters: host (-h, --host), port (-p, --port).
<br/>`python manage.py runprodserver`
 - **Help**: print the commands with their description.
<br/>`python manage.py -?`
<br/>It could be used with others commands to get more info of them. For example:
<br/>`python manage.py runserver -?`

### App.py

[app.py](application/app.py) controls the flask server in production and development mode. The differents URIs and methods that are in the server are:
 - **Login**: manage the user sessions.
 	- /login : the user log in the server.
 		- Method: GET
 		- Request: basic authorization header from a user.
 		- Response: json object with the username, email, project, project_description, access_token and refresh_token.
 		- Status code: 200
 	- /logout : the user logout of the server.
 		- Method: DELETE
 		- Request: bearer token of a user.
 		- Response: json object with a msg of success.
 		- Status code: 200
 	- /changepassword : the user changes his password.
 		- Method: PUT
 		- Request: bearer token of a user and newpassword in the header.
 		- Response: json object with a msg of success.
 		- Status code: 200
 - **Dmp**: manage the data managment plan of the mongodb.
 	- /dmps : return all the dmps of a user.
 		- Method: GET
 		- Request: bearer token of a user.
 		- Response: json object with a list of dmps.
 		- Status code: 200
 	- /dmps : create a new user dmp.
 		- Method: POST
 		- Request: bearer token of a user and a dmp (json) in the body.
 		- Response: json object with a msg of success and the id of the dmp generated.
 		- Status code: 201
 	- /dmps/<dmp_id> : return the dmp with the dmp_id of a user.
 		- Method: GET
 		- Request: bearer token of a user.
 		- Response: json object the requested dmp.
 		- Status code: 200
 	- /dmps/<dmp_id> : return the dmp with the dmp_id of a user.
 		- Method: PUT
 		- Request: bearer token of a user and a json in the body with the keys and values that need to be updated.
 		- Response: json object with a msg of success and the id of the dmp updated.
 		- Status code: 200
 	- /dmps/<dmp_id> : delete a dmp with the dmp_id of a user.
 		- Method: DELETE
 		- Request: bearer token of a user.
 		- Response: json object with a msg of success and the id of the dmp deleted.
 		- Status code: 200
 - **Task**: manage the task of the mongodb.
 	- /tasks : return all the task in descending order of creation. It could be flter by the status and/or dmp id parameter.
 		- Method: GET
 		- Request: bearer token of a user and an optional status and dmp id parameters.
 		- Response: json object with all the requested tasks.
 		- Status code: 200
 	- /tasks : create a new task.
 		- Method: POST
 		- Request: bearer token of a user and a task (json) in the body.
 		- Response: json object with a msg of success and the id of the task generated.
 		- Status code: 201
 - **File**: send files of the dmp.
 	- /resources/docx/<file_id> : return the file_id.docx file.
 		- Method: GET
 		- Request: bearer token of a user.
 		- Response: file_id.docx file.
 		- Status code: 200
 	- /resources/pdf/<file_id> : return the file_id.pdf file.
 		- Method: GET
 		- Request: bearer token of a user.
 		- Response: file_id.pdf file.
 		- Status code: 200
 - **Token**: manage user tokens.
 	- /refresh : return the file_id.docx file.
 		- Method: GET
 		- Request: refresh token of a user.
 		- Response: json object with a new access_token.
 		- Status code: 200
 - **Test**: some test routes that will be deleted in the future.

### Models.py

[models.py](application/models.py) contains the model for the tables of the sql database. As you can see in the image, the differents tables of the database are:
<p align="center">  <img src="https://i.ibb.co/PhP74N9/Modelsqlite.png">  </p>

 - **user**: table of the users of the api.
 	- id: primary key of the user (Integer).
 	- username: name of the user (String, unique and no nulleable).
 	- password_hash: hashcode of the user's password (String and no nulleable).
 	- email: email of the user, by default is none (String).
 	- admin: defines if the user has admin permissions by default is false (Boolean).
 - **project**: table of the projects of the api.
 	- id: primary key of the user (Integer).
 	- name: name of the user (String, unique and no nulleable).
 	- description: description of the project, by default is none (Text).
 - **user_project**: table of the relation Many-to-Many of the users and projects.
 	- id_user: foreign key of the user (Integer).
 	- id_project: foreign key of the project (Integer).

### Config.py

[config.py](application/config.py) configuration file of the server.





## Future tasks

- [x] Create README.md
- [ ] Finish README.md
- [ ] Delete test routes
- [X] Update timestamp in the creation of the task.
- [X] Filter task by id dmp.
- [X] Order task by timestamp.
 	

