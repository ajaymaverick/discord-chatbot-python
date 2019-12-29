'''
Provides single entry point for all other modules to access the SqlAlchemy instance

@author: ajay
'''
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()