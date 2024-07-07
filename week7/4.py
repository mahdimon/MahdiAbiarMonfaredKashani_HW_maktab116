import sys
sys.path.append("/home/mahdimon/programming/maktab/week7/moduls")
from auth import Authenticator
import exeptions as err

while True:
    command = input("""enter:
1 for signing up 
2 for signing in
3 for checking loged status
0 to end program: """)
    try:
        match command:
            case "0":
                break
            case "1":
                username = input("username: ")
                password = input("password: ")
                Authenticator.add_user(username,password)
            case "2":
                username = input("username: ")
                password = input("password: ")
                Authenticator.login(username,password)
            case "3":
                username = input("username: ")
                print(f"{username} is{'' if Authenticator.is_logged_in(username) else ' not'} logged in")
    except err.AuthExeption as e:
        print("error:",type(e).__name__)