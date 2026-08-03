from login import login
from register import register
from view_users import view_users

print("====================================")
print("   Smart Society Apartment System   ")
print("====================================")

while True:
    print("\n1. Login")
    print("2. Register")
    print("3. View Users")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        login()

    elif choice == "2":
        register()

    elif choice == "3":
        view_users()

    elif choice == "4":
        print("\nApplication Closed")
        break

    else:
        print("\nPlease enter a valid choice.")