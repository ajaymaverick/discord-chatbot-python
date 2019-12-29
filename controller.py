'''
Controller class which contains all the business logic

@author: ajay
'''

from database import db
from models import search_history
import datetime
from sqlalchemy import and_


from googlesearch import search


def getGoogleSearchResult(query):
    '''
    Provides top 5 search results for given query using google search API
    '''
    search_result_list = list(search(query, num=5, stop=5, pause=1))
    return search_result_list

def getSearchHistory(username, searchPattern):
    '''
    Provides recent search items for a given users based on given search String
    '''
    tag = '%' + searchPattern + '%'
    print(tag)
    search_result = db.session.query(search_history).filter(and_(search_history.user_name == username, search_history.search_query.like(tag))).order_by(search_history.query_date.desc()).all()
        
    resList = []
    for search in search_result:
        resList.append(search.search_query)
           
    return resList

def storeSearchHistory(username, searchQuery):
    '''
    Updates search history table for the given user, Makes sure that new entry doesn't exist 
    in database before inserting in order to avoid duplicate records.
    '''
    if checkIfExists(username, searchQuery) == False:
        search_his=search_history(user_name=username,search_query=searchQuery,query_date=datetime.datetime.utcnow())
        db.session.add(search_his)
        db.session.commit()
    

def checkIfExists(username, searchQuery):
    '''
    Checks if the given seach query for a given users already exists or not in the table
    '''
    search_query = db.session.query(search_history).filter(and_(search_history.user_name == username, search_history.search_query == searchQuery))
    if search_query.count() > 0:
        return True
    else:
        return False
        
    
    