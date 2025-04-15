from services.user_dao import create_user, password_match, get_user_id

username = input("Enter username: ")
password = input("Enter password: ")

user_id = None

if password_match(username, password):
    print("Password match")
    user_id = get_user_id(username)
else:
    print("Invalid username or password.")

if user_id:
    print(f"Logged in as user ID: {user_id}")
