import re
from uuid import uuid1
import getpass
from hashlib import sha256
class User:
    users = {}
    def __str__(self):
        return f"""user name:{self.username}
phone number: {self.phone_number}
id: {self.id}"""
    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self,value):
        MIN_LENGTH = 4
        ALLOWED_CHARS = r"^[a-zA-Z0-9]+$"
        errors = []
        if len(value) < MIN_LENGTH:
            errors.append(f"Username must be at least {MIN_LENGTH} characters long")
        if not re.match(ALLOWED_CHARS, value):
            errors.append("Username can only contain letters and numbers")
        if not errors and value in self.users:
            errors.append("this user name is taken choose a diffrent one")
        if errors:
            raise ValueError(errors)
        self.__username = value
    
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,value):
        self.__id = value 
   
    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self,value:str):
        errors = []
        PATTERN =  r"(?=^.{4,}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])"
        if not re.match(PATTERN, value):
            errors.append("password must be 4 characters long and have at least one uppercase one lower case and one digit")
        if errors:    
            raise ValueError(errors)
        
        self.__password = sha256(value.encode())
    
    @property
    def phone_number(self):
        return self.__phone_number
    
    @phone_number.setter
    def phone_number(self,value):
        errors = []
        PATTERN =  r"^09\d{9}$"
        if not re.match(PATTERN, value):
            errors.append("enter a valid phone number")
        if errors:    
            raise ValueError(errors)
        self.__phone_number = value


   
    
    @classmethod
    def sign_up(cls):
        items = ["username","password","phone_number"]
        new = cls()
        print('you are signing up')
        for item in items:
            while True:
                try:
                    prompt = f"set your {item}: "
                    value = getpass.getpass(prompt) if item == "password" else input(prompt)
                    setattr(new,item,value) 
                    break
                except ValueError as e:
                    [print(i) for i in e.args[0]]
                    
                except EOFError:
                    return
        new.id = uuid1()
        cls.users[new.username]=new
        print("signing up was succssesful")
    
    @classmethod
    def sign_in(cls):
        while True:
            try:
                username = input("enter your user name:  ")
                user:User = cls.users[username]
                break
            except EOFError:
                return False
            except KeyError:
                print("this username does not exist")
        for i in range(3,0,-1):
            try:
                password = getpass.getpass("enter you password ")
            except EOFError:
                return False
            if sha256(password.encode()).hexdigest() == user.password.hexdigest():
                print("\nyou are not loged in")
                return user
            else:
                print(f"wrong password you have {i-1} more chance " if i> 1 else "you have no attempts left") 
        return False    
    def modify(self):
        items = ["username","phone_number"]
        for item in items:
            while True:
                try:
                    value = input(f"set your {item} (enter 0 if you dont want to change it): ")
                    if value == "0": break
                    old_username = self.username 
                    setattr(self,item,value)
                except ValueError as e:
                    [print(i) for i in e.args[0]]
                except EOFError:
                    return
                else:
                    del self.__class__.users[old_username]
                    self.__class__.users[self.username] = self
                    break
    @staticmethod
    def is_valid_password(value):
        PATTERN =  r"(?=^.{4,}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])"
        if re.match(PATTERN, value):
           return True
        return False
    
    def change_password(self):
        hash = self.password.hexdigest()
        while True:
            try:
                old_password = getpass.getpass("old password: ")
            except EOFError:
                return    
            if sha256(old_password.encode()).hexdigest() == hash : break
            else: print("wrong password")
        while True:
            try:
                new_password = getpass.getpass("new password: ")
            except EOFError:
                return
            if self.is_valid_password(new_password):
                break
            else:
                print("password must be 4 characters long and have at least one uppercase one lower case and one digit")
        while True:
            try:
                second_new_password = getpass.getpass("re enter new password: ")
            except EOFError:
                return
            if second_new_password ==  new_password:
                break
            else:
                print("the passwords dosent match")
        self.password = new_password
            
        
                
                
        
                
            
        
    
while True:
    command = input("enter 1 for signing up and 2 for signing in and 0 to end program: ")
    match command:
        case "0":
            break
        case "1":
            User.sign_up()
        case "2":
            user = User.sign_in()
            if not user: continue
            while True:
                command = input("""\nenter:
1 for seeing your data
2 for changing phone number or username
3 for changing password
4 for returning to main menu\n""")
                match command:
                    case "1":print(user)                        
                    case "2":user.modify() 
                    case "3":user.change_password()                       
                    case "4": break
                       
        