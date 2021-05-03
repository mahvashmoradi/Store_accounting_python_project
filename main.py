from User import Admin, Customer


def welcome():
    """
    This function is for welcome to users
    """
    print("------------------------------------------------------------------------------------------")
    print("----------------------------------Well Come to Our Shop-----------------------------------")
    print("------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    # init_logging()
    welcome()
    Admin.admin_init()
    while True:
        if Admin.verify_admin():
            # verify_admin and if it is ok, leads to menu
            pwd = input("please set your password")
            admin = Admin.create_account('admin', pwd)
            print("Your account is created. please log in")
            break
        else:
            continue

    while True:
        # select which of user? Customer,Admin or new Customer
        print("Who Are You?\nif you have an account please enter your name or enter n to create a new account")
        select = input()
        if select == "admin":
            print("please enter your password")
            if admin.log_in():
                while True:
                    # select the task
                    print("What want do you do")
                    break
            else:
                continue
        elif select == 'n':
            name = input("Please enter your name")
            with open("user_info.csv", 'r') as read:
                list_name = read.read()
                # try:
                while True:
                    if name in list_name:
                        # except AssertionError:
                        print("This name is exist")
                        name = input("Please enter other name")
                    else:
                        break
            pwd = input("please enter your password")
            name = Customer.create_account(name, pwd)
            print("Your account is created. please log in")
        else:
            # try:
            with open("user_info.csv", 'r') as read:
                # chek the name is not exist in customers name
                list_name = read.read()
                # try:
                if select in list_name:

                    print(f"well come {select}")
                    print("please enter your password")
                    name = Customer(select)
                    if name.log_in():
                        while True:
                            # select menu
                            print("have a good time")
                            break
                    else:
                        continue
                else:
                    print("There is not your account, Please create account")
                    continue
            """except:
                print("Please report this problem to admin")
                continue"""
