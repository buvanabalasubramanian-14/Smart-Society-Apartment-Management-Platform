from dashboard import dashboard

def login():

    print("\n===== Login =====")

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        file = open("../database/users.txt", "r")

        for line in file:

            details = line.strip().split(",")

            if email == details[3] and password == details[4]:

                print("\nLogin Successful!")
                print("Welcome", details[0])

                file.close()

                dashboard(details[0])

                return

        file.close()

        print("\nInvalid Email or Password")

    except FileNotFoundError:

        print("\nNo registered users found.")