import argparse
from models import User, Message
import psycopg2
from Hash_password import check_password

database_name = "example_database"
connection = psycopg2.connect(user="postgres", password="coderslab", host="localhost", database=database_name)
cursor = connection.cursor()
connection.autocommit = True

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (minimum 8 characters)")
parser.add_argument("-t", "--to", help="receiver of the message")
parser.add_argument("-s", "--send", help="text input")
parser.add_argument("-l", "--list", help="list of messages for a user", action="store_true")

args = parser.parse_args()

if args.username and args.password and args.list:
    user = User.load_user_by_username(cursor, args.username)
    if user is None:
        print("There is no such user!")
    else:
        if check_password(args.password, user.hashed_password):
            messages = Message.load_all_messages(cursor, user.id)
            for message in messages:
                print("Receiver: " + message.to_id + "Data: " + message.creation_data + "Text: " + messages.text + "\n")
        else:
            print("There is no such user! (Pass)")
elif args.list:
    messages = Message.load_all_messages(cursor)
    for message in messages:
        print(
            "Sender:" + message.from_id + "\n" "Receiver: " + message.to_id + "\n" + "Data: " + message.creation_data + "\n" + "Text: " + messages.text + "\n" + "-------------")
elif args.username and args.password and args.to and args.send:
    user = User.load_user_by_username(cursor, args.username)
    if user is None:
        print("There is no such user!")
    else:
        if check_password(args.password, user.hashed_password):
            to_user = User.load_user_by_username(cursor, args.to)
            if to_user is None:
                print("Receiver does not exist")
            else:
                if len(args.send) > 255:
                    print("Message is too long!")
                else:
                    message = Message(user.id, to_user.id, str(args.send))
                    message.save_to_db(cursor)

        else:
            print("There is no such user! (Pass)")
