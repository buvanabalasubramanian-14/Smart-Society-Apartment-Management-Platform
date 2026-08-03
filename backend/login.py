def login():

    print("\n===== Login =====")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    try:
        file = open("../database/users.txt", "r")
        for line in file:
            user = line.strip().split(",")
            if user[3] == email and user[4] == password:
                print("\nLogin Successful!")
                print("Welcome", user[0])
                file.close()
                return
        file.close()
        print("\nInvalid Email or Password")
    except:
        print("\nNo users found.")