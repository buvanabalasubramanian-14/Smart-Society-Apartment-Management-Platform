def dashboard(name):
     while True:
        print("\n===== Dashboard =====")
        print("Welcome", name)
        print("\n1. View Profile")
        print("2. Maintenance Status")
        print("3. Logout")
        choice = input("\nEnter your choice: ")
        if choice == "1":
            print("\n----- My Profile -----")
            print("Resident Name :", name)
        elif choice == "2":
            print("\nMaintenance Status")
            print("No Pending Dues")
        elif choice == "3":
            print("\nYou have logged out successfully.")
            break
        else:
            print("\nInvalid choice. Please try again.")