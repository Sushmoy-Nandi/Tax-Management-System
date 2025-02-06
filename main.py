from register_user import register_user
from dashBoard import user_dashboard
from user_login import login_user
from admin_dash_board import admin_dashboard


def main():
    # Main function to handle user interaction and authentication.
    while True:
        print("\n=== Tax Management System ===")
        print("1. User Signup")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Exit")

        role = input("Enter your choice (1-4): ")

        try:
            if role == "1":
                # User Signup
                register_user()

            elif role == "2":
                # User Login
                login_result=login_user()
                if login_result:
                    user_nid, name = login_result 
                    print(f"\nLogin successful! Welcome, User {user_nid}\nHello {name}.\nWelcome to Tax Management System")
                    user_dashboard(user_nid)
                else:
                    print("Login failed. Please try again.")

            elif role == "3":
                # Admin Login
                admin_dashboard() 

            elif role == "4":
                # Exit the application
                print("Thank you for using the Tax Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please select an option from 1 to 4.")

        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

if __name__ == "__main__":
    main()
