
from functools import cached_property, lru_cache
from schemas.User import User
from typing import List


## This singleton class acts as a database of users 
## The usual case would be that this class connects to a database table and perform queries. However, since we are simulating a mock server for testing, the below is demeed enough
class Users:
    table: List[User] = []


    class __Users:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not Users.instance:
            Users.instance = Users.__Users(arg)
        else:
            Users.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)
    
    @staticmethod
    def addUser(user: User):
        Users.table.append(user)

    @staticmethod
    def updateUser(email:str,user: User):
        for i,u in enumerate(Users.table):
            if u.email == email:
                Users.table[i] = user
        

    @staticmethod
    def removeUserByEmail(email:str):
        user = Users.getUserByEmail(email)
        if user:
            Users.table.remove(user)

    @staticmethod
    def getUserByEmail(email: str):
        for user in Users.table:
            if user.email == email:
                return user
    
    @staticmethod
    def getUsers(offset: int,limit: int):
        if(offset >= 0 and limit > 0):
            return Users.table[offset:limit]
        return Users.table
    

    @staticmethod
    def clearUsers():
        Users.table.clear()
