from User import Admin, Customer
import pandas as pd


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
    file_path_account = "user_info.csv"
    try:
        df_account = pd.read_csv(file_path_account)
    except:
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
                if admin.log_in():
                    while True:
                        # select the task
                        print("What want do you do\n1-see product\n2-create_product\n3-see_order\n4-active_account\n"
                              "5-change password\n6-log out")
                        admin_menu = input()
                        if admin_menu == '1':
                            Admin.show_product()
                        elif admin_menu == '2':
                            df = pd.read_csv("Product_info.csv")
                            while True:
                                prod = input('Please enter the id,name,price,brand,quantity of products;'
                                             '\n enter e to exit: ').split(',')
                                print(prod)
                                if prod == ['e']:
                                    break
                                prod = [int(x.strip()) if x.isdigit() else x for x in prod]
                                if len(prod) == 5:
                                    if isinstance(prod[2], int) and isinstance(prod[4], int):
                                        df = Admin.create_product(df, prod)
                                    else:
                                        print("Wrong input")
                                        continue
                                else:
                                    print("Wrong input")
                                    continue
                            df.to_csv("Product_info.csv", mode='w', index=False, sep=",", header=True)
                            print(df.loc[:, ["name", "price", "brand", "quantity"]])
                        elif admin_menu == '3':
                            admin.see_orders()
                        elif admin_menu == '4':
                            a_name = input("please enter the name of account you want to active: ")
                            admin.active_account(a_name)
                            print(f"{a_name} account is active")
                        elif admin_menu == '5':
                            old_password = input("Please enter your old password")
                            new_password = input("Please enter new password")
                            print(admin.change_password(old_password, new_password))
                        elif admin_menu == '6':
                            break
                        else:
                            print("Wrong Input")
                else:
                    continue
            else:
                file_path_account = "user_info.csv"
                df_account = pd.read_csv(file_path_account)
                lst_username = list(df_account["username"])
                if username in lst_username:
                    welcome()
                    name = Customer(username)
                    if name.log_in():
                        print(f"well come {username}")
                        factor = pd.DataFrame({"name": [], "price": [], "num": [], "total": []})
                        factor.to_csv('factor.csv', index=False)
                        while True:
                            # select menu
                            print("What want do you do\n1-show and select product\n2-see your cards\n3-print factor\n"
                                  "4-change password\n5-log out")
                            menu_customer = input()
                            if menu_customer == '1':
                                df_product = pd.read_csv("Product_info.csv")
                                Customer.show_product(df_product)
                                print("select your item. enter space then the number of product you"
                                      " need\ntype f to finish :")
                                while True:
                                    product_num = input().split(' ')
                                    if product_num == ['f']:
                                        break

                                    if len(product_num) == 2:
                                        if product_num[0].isdigit() and product_num[1].isdigit():
                                            try:
                                                print(name.add_cards(df_product, int(product_num[0]), int(product_num[1])))
                                                # print()
                                            except:
                                                print("There is not such product")
                                        else:
                                            print("Invalid input")
                                            continue
                                    else:
                                        print("Invalid input")
                                        continue
                            elif menu_customer == '2':
                                Customer.see_cards()
                            elif menu_customer == '3':
                                s_factor = Customer.print_factor()
                                print(s_factor)
                                Customer.save_to_data(name.name, s_factor)
                                print("Thanks for your shopping")
                                factor = pd.DataFrame({"name": [], "price": [], "num": [], "total": []})
                                factor.to_csv('factor.csv', index=False)
                            elif menu_customer == '4':
                                old_password = input("Please enter your old password")
                                new_password = input("Please enter new password")
                                print(name.change_password(old_password, new_password))
                            elif menu_customer == '5':
                                break
                            else:
                                print("invalid input")
                    else:
                        continue
                else:
                    print("There is not your account, Please create account")
                    continue
        elif select == '2':
            name = input("Please set your username: ")
            file_path_account = "user_info.csv"
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
            print("Your account is created. please log in")
        else:
            print("invalid input")
