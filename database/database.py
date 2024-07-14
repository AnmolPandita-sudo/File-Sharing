import pymongo
from config import DB_URL, DB_NAME

# MongoDB client setup
dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]

user_data = database['users']


async def present_user(user_id: int, username: str = None, fname: str = None, lname: str = None):
    query = {
        '_id': user_id
    }
    if username:
        query['username'] = username
    if fname:
        query['first_name'] = fname
    if lname:
        query['last_name'] = lname

    user_document = user_data.find_one(query)
    return user_document is not None


async def add_user(user_id: int, username: str = None, fname: str = None, lname: str = None):
    user_filter = {'_id': user_id}  # Define user_filter for the query
    user_update = {
        '_id': user_id,
        'username': username if username else ' ',
        'first_name': fname if fname else ' ',
        'last_name': lname if lname else ' '
    }
    # Upsert the document: Update if exists, Insert if not exists
    user_data.update_one(user_filter, {'$set': user_update}, upsert=True)
    return


async def full_userbase():
    user_docs = user_data.find()
    users = []
    for doc in user_docs:
        user = {
            '_id': doc['_id'],
            'username': doc.get('username', ' '),
            'first_name': doc.get('first_name', ' '),
            'last_name': doc.get('last_name', ' ')
        }
        users.append(user)
    return users


async def del_user(user_id: int):
    result = user_data.delete_one({'_id': user_id})
    print(
        f"Deleted {result.deleted_count} document(s) with user_id: {user_id}")
    return
