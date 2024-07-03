from pymongo import MongoClient
from .config import bot_name,redis_db_number
from typing import Generator
import redis

r = redis.Redis(host='localhost', port=6379, db=redis_db_number, decode_responses=True)
client = MongoClient("localhost", 27017)
db = client[bot_name]
users = db["users"]
groups = db["groups"]


# privates db functions
def new_user(userID:int) -> bool:
    user = {'_id': userID}
    return users.insert_one(user) if not users.find_one(user) else None
    
def del_user(userID:int) -> bool:
    user = {'_id': userID}
    return users.delete_one(user) if users.find_one(user) else None
    
def find_user(userID:int) -> bool:
    user = {'_id': userID}
    return users.find_one(user)

def all_users() -> Generator:
    return users.find()



# groups db functions

def new_group(chatID:int) -> bool:
    find = groups.find_one({'_id': chatID})
    base = {"_id": chatID, "status": True, "admins": [], "commands": {}}
    if not find:
        return groups.insert_one(base)
    groups.delete_one({"_id": chatID})
    return groups.insert_one(base)

def del_group(chatID:int) -> bool:
    find = groups.find_one({'_id': chatID})
    if find:
        print('ttt')
        return groups.delete_one(find)  
    
    
def new_key(chatID: int, key: str, value):
    find = groups.find_one({"_id": chatID})
    if find:
        if key in find['commands']:
            if value in find['commands'][key]:
                return 0 # no because is existed
            else:
                groups.update_one({"_id": chatID}, {"$push": {f"commands.{key}": value}})
                return 1 # ok
        else:
            groups.update_one({'_id':chatID}, {'$set': {f'commands.{key}': [value]}})
            return 1 # ok
    else:
        new_group(chatID)
        groups.update_one({'_id':chatID}, {'$set': {f'commands.{key}': [value]}})
        return 1 # ok


def del_key(chatID:int, key:str) -> bool:
    find = groups.find_one({"_id": chatID})
    if find:
        if key in find['commands']:
            groups.update_one({'_id': chatID}, {'$unset': {f'commands.{key}': ''}})
            return True
        else:
            return False
    else:
        new_group(chatID)
        return False
    
    
def del_all_keys(chatID:int):
    find = groups.find_one({"_id": chatID})
    if find:
        if find['commands']:
            groups.update_one({'_id': chatID}, {'$unset': {f'commands': ''}})
            groups.update_one({"_id": chatID}, {"$set": {"commands": {}}})
            return True
        else:
            return False
    else:
        new_group(chatID)
        return False

def get_key(chatID:int, key:str) -> bool :
    find = groups.find_one({"_id": chatID})
    if find:
        if key in find['commands']:
            return find['commands'][key]
        else:
            return False
    else:
        new_group(chatID)
        return False

def get_all_key(chatID:int) -> bool:
    find = groups.find_one({"_id": chatID})
    if find:
        if find['commands']:
            return find['commands']
        else:
            return False
    else:
        new_group(chatID)
        return False 
    


