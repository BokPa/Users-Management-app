import argparse
from models import User
import psycopg2
from Hash_password import check_password

database_name = "example_database"
connection = psycopg2.connect(user="postgres", password="coderslab", host="localhost", database=database_name)
cursor = connection.cursor()
connection.autocommit = True

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (minimum 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (minimum 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete")
parser.add_argument("-e", "--edit", help="edit username")

args = parser.parse_args()


#edit user password
if args.username and args.password and args.edit and args.new_pass:
    user = User.load_user_by_username(cursor, args.username)
    if user is None:
        print("There is no such user!")
    else:
        if check_password(args.password, user.hashed_password):
            if len(args.new_pass) < 8:
                print("Password should have minimum 8 characters")
            else:
                user.set_password(args.new_pass)
                print("Password changed")
        else:
            print("There is no such user! (Pass)")
elif args.username and args.password and args.delete:
    user = User.load_user_by_username(cursor, args.username)
    if user is None:
        print("There is no such user!")
    else:
        if check_password(args.password, user.hashed_password):
            user.delete(cursor)
        else:
            print("There is no such user! (Pass)")
elif args.username and args.password:
    # add new user
    try:
        user = User(username=args.username, password=args.password)
        if len(args.password) < 8:
            print("Password should have minimum 8 characters")
        else:
            user.save_to_db(cursor)
    except psycopg2.errors.UniqueViolation:
        print(f"User {args.username} already exists")
elif args.list:
    users_list = User.load_all_users(cursor)
    for user in users_list:
        print(user.username)
else:
    parser.print_help()

connection.close()





