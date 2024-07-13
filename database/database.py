import pymongo
import os
from config import DB_URL, DB_NAME


dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]


user_data = database['users']


async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)


async def add_user(user_id: int, username=None, first_name=None, last_name=None):
    user_document = {
        '_id': user_id
    }

    if username is not None:
        user_document['username'] = username
    else:
        user_document['username'] = 'unavailable'

    if first_name is not None:
        user_document['first_name'] = first_name
    else:
        user_document['first_name'] = 'unavailable'

    if last_name is not None:
        user_document['last_name'] = last_name
    else:
        user_document['last_name'] = 'unavailable'

    user_data.insert_one(user_document)
    return


async def full_userbase():
    user_docs = user_data.find()
    users = []
    for doc in user_docs:
        user = {
            'id': doc['_id'],
            'username': doc.get('username', ''),
            'first_name': doc.get('first_name', ''),
            'last_name': doc.get('last_name', '')
        }
        users.append(user)
    return users


async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return
