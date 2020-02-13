from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer,\
    String, Text, Float
from sqlalchemy.orm import relationship, backref
from application.app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Projects(db.Model):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    description = Column(Text, nullable=True, default="none")

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(200), nullable=True, default="none")
    admin = Column(Boolean, nullable=False, default=False)

    projects = relationship("Projects", secondary="user_project", backref='users')

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


user_project = db.Table('user_project',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
