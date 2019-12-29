'''
Models class contains all definition of database tables which are accessed through
SqlAlchemy(JPA)

@author: ajay
'''

from database import db
from sqlalchemy import DateTime
import datetime

class search_history(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String())
    search_query = db.Column(db.String())
    query_date = db.Column(DateTime,  default=datetime.datetime.utcnow)

    def __init__(self, user_name, search_query, query_date):
        self.user_name = user_name
        self.search_query = search_query
        self.query_date = query_date
        