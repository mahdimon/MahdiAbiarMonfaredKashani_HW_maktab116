from hashlib import sha256
class User:
    login = False
    def __init__(self,username,password):
        self.username = username
        self.password = password
    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self,value):
        self.__username = value
        
    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self,value):
        self.__password = sha256(value.encode())
        