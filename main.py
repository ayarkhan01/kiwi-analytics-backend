from services.position_dao import get_positions_by_portfolio
from services.user_dao import password_match, get_user_id
from services.portfolio_dao import get_portfolios_by_user, get_portfolio_by_id

"""
admin = input("Enter username: ")
password = input("Enter password: ")
if password_match(admin, password):
    print("Login successful")
    user_id = get_user_id(admin)
    print(f"User ID: {user_id}")
else:
    print("Login failed")
"""
print(get_positions_by_portfolio(2))