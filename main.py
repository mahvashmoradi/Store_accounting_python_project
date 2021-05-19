from User import Admin, Customer
import pandas as pd
import logging


def welcome():
    """
    This function is for welcome to users
    """
    print("------------------------------------------------------------------------------------------")
    print("----------------------------------Well Come to Our Shop-----------------------------------")
    print("------------------------------------------------------------------------------------------")


def init_logging():
    # Create a custom logger
    admin_logger = logging.getLogger("admin")

    # Create handlers
    c_handler = logging.StreamHandler()
    fg_handler = logging.FileHandler('log_file.log')

    c_handler.setLevel(logging.WARNING)
    fg_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(asctime)s - %(message)s')
    fg_format = logging.Formatter('%(asctime)s - %(message)s')

    c_handler.setFormatter(c_format)
    fg_handler.setFormatter(fg_format)

    # Add handlers to the logger
    admin_logger.addHandler(c_handler)
    admin_logger.addHandler(fg_handler)

    admin_logger.info('This is info test')
    admin_logger.error('This is error test')
    admin_logger.warning("This is warning test")
    admin_logger.debug("This is debug test")
    return admin_logger


if __name__ == '__main__':
    admin_logger = init_logging()
    welcome()
    file_path_account = "user_info.csv"
    file_path_product = "Product_info.csv"
    try:
        df_account = pd.read_csv(file_path_account)
    except FileNotFoundError:
        Admin.first_init()
    else:
        lst_username = list(df_account["username"])
        if "admin" not in lst_username:
            # chek the admin is registered. If not, create the admin account
            pwd = input("Hi Admin,\nplease set your password: ")
            admin = Admin.create_account('admin', pwd)
            print("Your account is created. please log in")
    while True:
        print("Who Are You?\nif you have an account please login or create a new account")
        select = input("1-log in\n2-sign up\nyou select: ")
        if select == "1":
            # select log in or sign up
            username = input("Please enter your username: ")
            if username == 'admin':
                # chek the input is admin or customer
                print("Hi Admin")
                admin = Admin("admin")
                df_account = pd.read_csv(file_path_account)
                count = 0
                while count < 3:
                    passwd = input("Please enter your password: ")
                    if admin.chek_pass(passwd, df_account):
                        login = True
                        break
                    else:
                        count += 1
                        print("Wrong Password")
                else:
                    login = False
                    print('You entered the password in 3 times. Please try later')
                if login:
                    admin_logger.warning("Admin is log in")
                    while True:
                        # select the task
                        print("What want do you do\n1-see all product\n2-see finished product\n3-create_product\n"
                              "4-see_order\n5-active_account\n6-change password\n7-log out")
                        admin_menu = input()
                        df_product = pd.read_csv(file_path_product)
                        if admin_menu == '1':
                            Admin.show_product(df_product)
                        elif admin_menu == '2':
                            Admin.show_finished_product(df_product)
                        elif admin_menu == '3':
                            while True:
                                prod = input('Please enter the id,name,price,brand,quantity of products;'
                                             '\n enter e to exit: ').split(',')
                                print(prod)
                                if prod == ['e']:
                                    break
                                prod = [x.strip() for x in prod]
                                prod = [int(x) if x.isdigit() else x for x in prod]
                                if len(prod) == 5:
                                    if isinstance(prod[2], int) and isinstance(prod[4], int):
                                        df_product = Admin.create_product(df_product, prod)
                                    else:
                                        print("The values are incorrect")
                                        continue
                                else:
                                    print("Wrong input")
                                    continue
                            admin_logger.warning("The new products is defined")
                            df_product.to_csv(file_path_product, mode='w', index=False, sep=",", header=True)
                            print(df_product.loc[:, ["name", "price", "brand", "quantity"]])
                        elif admin_menu == '4':
                            admin.see_orders()
                        elif admin_menu == '5':
                            a_name = input("please enter the name of account you want to active: ")
                            admin.active_account(df_account, a_name)
                            print(f"{a_name} account is active")
                            admin_logger.warning(f"customer {a_name} account is active")
                        elif admin_menu == '6':
                            old_password = input("Please enter your old password: ")
                            new_password = input("Please enter new password: ")
                            ch_pass_status = admin.change_password(df_account, old_password, new_password)
                            print(ch_pass_status)
                            if ch_pass_status == "Your password is changed":
                                admin_logger.warning("Admin password is changed")
                        elif admin_menu == '7':
                            admin_logger.warning("Admin is log out")
                            break
                        else:
                            print("Wrong Input")
                else:
                    admin_logger.error("The admin password is entered 3 times in wrong, Is it admin?")
                    continue
            else:
                df_account = pd.read_csv(file_path_account)
                lst_username = list(df_account["username"])
                if username in lst_username:
                    welcome()
                    name = Customer(username)
                    count = 0
                    try:
                        # chek status of account
                        assert list(df_account.loc[df_account["username"] == name.name, "status_account"])[0]
                        while count < 3:
                            passwd = input("Please enter your password: ")
                            if name.chek_pass(passwd, df_account):
                                login = True
                                break
                            else:
                                count += 1
                                print("Wrong Password")
                        else:
                            login = False
                            name.close_account(df_account, name.name)
                            print("Your account is closed")
                            admin_logger.warning(f"customer {name.name} account is closed")
                    except AssertionError:
                        print("Your account is closed\nplease report this problem to admin")
                        login = False
                    if login:
                        print(f"well come {username}")
                        admin_logger.warning(f"customer {username} is log in")
                        df_factor = pd.DataFrame({"name": [], "price": [], "num": [], "total": []})
                        save = False
                        while True:
                            # select menu
                            print("What want do you do\n1-show and select product\n2-see your cards\n3-print factor\n"
                                  "4-change password\n5-log out")
                            menu_customer = input()
                            df_product = pd.read_csv(file_path_product)
                            if menu_customer == '1':
                                print(Customer.show_product(df_product))
                                print("select your item. enter space then the number of product you"
                                      " need\ntype f to finish :")
                                while True:
                                    product_num = input().split(' ')
                                    if product_num == ['f']:
                                        df_product_save = df_product
                                        break
                                    if len(product_num) == 2:
                                        if product_num[0].isdigit() and product_num[1].isdigit():
                                            try:
                                                status_chek_quantity = name.chek_quantity(df_product,
                                                                                          int(product_num[0]),
                                                                                          int(product_num[1]))
                                                print(status_chek_quantity[1])
                                                if status_chek_quantity[0]:
                                                    df_product, df_factor = name.add_cards(df_product, df_factor,
                                                                                           int(product_num[0]),
                                                                                           int(product_num[1]),
                                                                                           admin_logger)
                                            except:
                                                print("There is not such product")
                                        else:
                                            print("Invalid input")
                                            continue
                                    else:
                                        print("Invalid input")
                                        continue
                            elif menu_customer == '2':
                                print(Customer.see_cards(df_factor))
                            elif menu_customer == '3':
                                s_factor = Customer.print_factor(df_factor)
                                print(s_factor)
                                Customer.save_to_data(name.name, s_factor)
                                admin_logger.warning(f"The new factor by customer {name.name}")
                                print("Thanks for your shopping")
                                df_factor = pd.DataFrame({"name": [], "price": [], "num": [], "total": []})
                                # factor.to_csv('factor.csv', index=False)
                                save = True
                            elif menu_customer == '4':
                                old_password = input("Please enter your old password: ")
                                new_password = input("Please enter new password: ")
                                ch_pass_status = name.change_password(df_account, old_password, new_password)
                                print(ch_pass_status)
                                if ch_pass_status == "Your password is changed":
                                    admin_logger.warning(f"customer {name.name} password is changed")
                            elif menu_customer == '5':
                                admin_logger.warning(f"customer {username} is log out")
                                # print(df_product_save)
                                if save:
                                    # df_product.to_csv(file_path_product, index=False)
                                    df_product_save.to_csv(file_path_product, mode='w', index=False, sep=",",
                                                           header=True)
                                break
                            else:
                                print("invalid input")
                    else:
                        admin_logger.warning(f"customer {username} is try to log in")
                        continue
                else:
                    print("There is not your account, Please create account")
                    continue
        elif select == '2':
            name = input("Please set your username: ")
            df_account = pd.read_csv(file_path_account)
            lst_username = list(df_account["username"])
            while True:
                if name in lst_username:
                    print("This username is exist")
                    name = input("Please enter other username: ")
                else:
                    break
            pwd = input("please set your password: ")
            name = Customer.create_account(name, pwd)
            admin_logger.warning(f"The new customer with name {name.name}")
            print("Your account is created. please log in")
        else:
            print("invalid input")
