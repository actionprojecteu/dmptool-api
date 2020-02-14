# DMPTOOL-API


## What is it?

dmptool-api is the backend of the [dmptool application](https://github.com/actionprojecteu/dmptool), which it generates data managment plans for the [ACTION](https://actionproject.eu/) projects.


## Files

The api files in order are:
 - application:
 	- [app.py](application/app.py) : controls the requests and responses of the server.
 	- [config.py](application/config.py) : contains the differents configurations for the server.
 	- [models.py](application/models.py) : contains the model for the tables of the sql database.
 	- [resources.py](application/resources.py) : resources for the api (*empty for the moment*).
 - db:
 	- [dbase.db](db/dbase.dbd) : database sqlite3 for users and projects.
 - [manage.py](manage.py) : main python file with several command options for managing the database and starting the server.
 - [Dockerfile](Dockerfile) : file for dockerize the api.
 - [requeriments.txt](requeriments.txt) : the libraries needed for the proper operation of the server.

## Command line methods

The [manage.py](manage.py) file, which it is the main python file of the api, allows to manipulate the database and start the server with the command line. Possibles functions are:
 - **Manage tables**: manages the tables of the sql database.
 	- Create tables: creates the tables of the sql database.
<br/>`python manage.py create_tables`
 	- Delete tables: deletes all the tables of the sql database (**Deletes all data**).
<br/>`python manage.py drop_tables`
 - **Manage users**: manages the user of the sql database.
 	- Create a normal user: username, password and email is required (promt input).
<br/>`python manage.py create_user`
 	- Create an admin user: username, password and email is required (promt input).
<br/>`python manage.py create_admin`
 	- Delete a user: username is required (promt input).
<br/>`python manage.py delete_user`
 - **Manage projects**: manages the projects of the sql database.
 	- Create a project: project and description is required (promt input).
<br/>`python manage.py create_user`
 	- Delete a project: project is required (promt input).
<br/>`python manage.py delete_user`
 - **Manage user-project relationship**: manages the relaion many-to-many between users and projects of the sql database.
 	- Create a user-project relationship: username and project name is required (promt input).
<br/>`python manage.py create_relation`
 	- Delete a user-project relationship: username and project name is required (promt input).
<br/>`python manage.py delete_relation`
 - **Start server**: starts the python server from app.py.
 	- Development mode: starts the development server. Optionals parameters: host (-h, --host), port (-p, --port).
<br/>`python manage.py runserver`
 	- Production mode: starts the production server. Optionals parameters: host (-h, --host), port (-p, --port).
<br/>`python manage.py runprodserver`
 - **Help**: prints the commands with their description.
<br/>`python manage.py -?`
<br/>It could be used with others commands to get more info of them. For example:
<br/>`python manage.py runserver -?`

## Server routes

The [app.py](application/app.py) file controls the flask server in production and development mode. The differents URIs and methods allowed in the server are:
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
 	- /tasks/<task_id> : return the task with the task_id.
 		- Method: GET
 		- Request: bearer token of a user.
 		- Response: json object the requested task.
 		- Status code: 200
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

## Database Model

The [models.py](application/models.py) file contains the model for the tables of the sql database. As you can see in the image, the differents tables of the database are:
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

## Configuration and dependencies

The [config.py](application/config.py) is the configuration file of the server. It contains the parameters for the CORS, JWT tokens, path or connection to the mongodb and sqlite3.

The [Dockerfile](Dockerfile) file contains the specifics to build a Docker image. For build the image, you need to execute the following command in the project folder:
<br/>`sudo docker build -t dmptool-api .`
<br/>Before running the image, we need to create a mongo docker where the dmps and images will be saved:
<br/>`docker run -d -p 27017:27017 --name mongodb mongo`
<br/>Lastly, we run the docker image mapping the log, dbase and document folders to the host machine, and connecting the docker to our mongo docker:
<br/>`docker run --name mydmptool-api -v /var/log/dmptool:/opt/log -v /home/dmptool/dbase-dmptool:/opt/db -v /home/dmptool/documents-dmptool:/opt/documents -p 5000:5000 --link mongodb:mongo -d dmptool-api`


The [requeriments.txt](requeriments.txt) contains the python libraries needed for the proper operation of the server. They could be installed by:
<br/>`pip install -r requeriments.txt`


<br/>
<br/>
<br/>
<br/>
<br/><br/><br/><br/><br/><br/><br/><br/>

## Future tasks

- [x] Create README.md
- [X] Finish README.md
- [ ] Delete test routes
- [X] Update timestamp in the creation of the task.
- [X] Filter task by id dmp.
- [X] Order task by timestamp.
 	

