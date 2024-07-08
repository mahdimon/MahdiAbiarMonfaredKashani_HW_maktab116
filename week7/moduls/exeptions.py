class AuthExeption(Exception):
    pass


class UsernameAlreadyExists(AuthExeption):
    pass


class PasswordTooShort(AuthExeption):
    pass


class InvalidUsername(AuthExeption):
    pass


class InvalidPassword(AuthExeption):
    pass
