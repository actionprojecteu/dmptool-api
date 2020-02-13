from flask_script import Manager, prompt_bool
from application.app import app, db
from application.models import *
from getpass import getpass

manager = Manager(app)
app.config['DEBUG'] = True


@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()
    db.session.commit()

@manager.command
def drop_tables():
    "Drop all project relational database tables. THIS DELETES ALL DATA."
    if prompt_bool("Are you sure you want to lose all your data:"):
        db.drop_all()


@manager.command
def create_admin():
    "Create an admin user."
    user = {"username": input("Username:"),
               "password": getpass("Password:"),
               "email": input("Email:"),
               "admin": True}
    usu = Users(**user)
    db.session.add(usu)
    db.session.commit()

@manager.command
def create_user():
    "Create a normal user."
    user = {"username": input("Username:"),
               "password": getpass("Password:"),
               "email": input("Email:"),
               "admin": False}
    usu = Users(**user)
    db.session.add(usu)
    db.session.commit()

@manager.command
def delete_user():
    "Delate a user."
    username= input("Username:")
    user = Users.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()


@manager.command
def create_project():
    "Create a project."
    project = {"name": input("Name:"),
               "description": input("Description:")}
    pro = Projects(**project)
    db.session.add(pro)
    db.session.commit()

@manager.command
def delete_project():
    "Delate a project."
    projectname= input("Username:")
    project = Projects.query.filter_by(name=projectname).first()
    db.session.delete(project)
    db.session.commit()


@manager.command
def create_relation():
    "Relation a user with a project."
    user = Users.query.filter_by(username=input("Username:")).first()
    project = Projects.query.filter_by(name=input("Project Name:")).first()
    user.projects.append(project)
    db.session.commit()

@manager.command
def delete_relation():
    "Delete relation of a user with a project."
    user = Users.query.filter_by(username=input("Username:")).first()
    project = Projects.query.filter_by(name=input("Project Name:")).first()
    user.projects.remove(project)
    db.session.commit()


@manager.command
@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', default=5000)
def runprodserver(host='0.0.0.0',port=5000):
    'Run flask server in a production enviroment with host 0.0.0.0 and port 5000 by default.'
    from waitress import serve
    serve(app, host=host, port=port)


if __name__ == '__main__':
    manager.run()
