def view_users():
    print("\nRegistered Residents\n")
    try:
        file = open("../database/users.txt", "r")
        for line in file:
            data = line.strip().split(",")
            print("Name :", data[0])
            print("Flat Number :", data[1])
            print("Phone Number :", data[2])
            print("Email :", data[3])
            print("-------------------------")
        file.close()
    except:
        print("No residents found.")