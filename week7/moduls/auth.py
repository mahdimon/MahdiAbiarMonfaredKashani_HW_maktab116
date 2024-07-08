from hashlib import sha256
from user import User
import exeptions as err


class Authenticator:
    users = {}

    @classmethod
    def add_user(cls, username, password):
        if username in cls.users:
            raise err.UsernameAlreadyExists
        if len(password) < 8:
            raise err.PasswordTooShort
        new = User(username, password)
        cls.users[username] = new

    @classmethod
    def login(cls, username, password):
        try:
            user: User = cls.users[username]
            assert sha256(password.encode()).hexdigest(
            ) == user.password.hexdigest()
        except KeyError:
            raise err.InvalidUsername from None
        except AssertionError:
            raise err.InvalidPassword from None
        else:
            user.login = True
            print("user logged in")

    @classmethod
    def is_logged_in(cls, username):
        try:
            return cls.users[username].login
        except KeyError:
            raise err.InvalidUsername
