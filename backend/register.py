def register():

    print("\n===== Registration =====")

    name = input("Enter your name: ")
    flat_no = input("Enter your flat number: ")
    phone = input("Enter your phone number: ")
    email = input("Enter your email: ")
    password = input("Create a password: ")

    file = open("../database/users.txt", "a")

    file.write(name + "," + flat_no + "," + phone + "," + email + "," + password + "\n")

    file.close()

    print("\nRegistration Successful!")
    print("Details Saved Successfully")