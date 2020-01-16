from flask_script import Manager
from aplicacion.app import app, db
from aplicacion.models import *
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
    "Drop all project relational database tables. THIS DELETES DATA."
    db.drop_all()


@manager.command
def create_admin():
    "Create an admin user."
    usuario = {"username": input("Username:"),
               "password": getpass("Password:"),
               "email": input("Email:"),
               "admin": True}
    usu = Usuarios(**usuario)
    db.session.add(usu)
    db.session.commit()

@manager.command
def create_user():
    "Create a normal user."
    usuario = {"username": input("Username:"),
               "password": getpass("Password:"),
               "email": input("Email:"),
               "admin": False}
    usu = Usuarios(**usuario)
    db.session.add(usu)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
