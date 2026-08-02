from login import login
print("===================================")
print(" Smart Society Apartment System ")
print("===================================")
print("1. Login")
print("2. Register")
print("3. Exit")
choice = input("Enter your choice: ")
if choice =="1":
    login()
elif choice == "2":
    print("Welcome to Registration Page")
elif choice == "3":
    print("Application Closed")
else:
    print("Please enter a valid choice")