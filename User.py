import json
import csv
import pandas as pd
import hashlib


def chek_pass(name):
    """
    This function gives the name of user and return the status of account and password to chek the login
    :param name: name of user
    :return: password and status of account
    """
    with open("user_info.csv", 'r', newline='') as reader:
        csv_reader = csv.DictReader(reader)
        sentence = [{"password": x['password'], "status_account": x["status_account"]} for x in csv_reader if
                    x['username'] == name]
        return sentence


class User:
    """
    The class User which have 2 child class(Admin and Customer)
    """

    def __init__(self, name):
        """

        :param name: name of user
        """
        self.name = name

    @classmethod
    def create_account(cls, name, pwd):
        """
        The class method to create a user and write the info of user on user_info.csv file
        :param name: name of user
        :param pwd: password of user
        :return: class
        """
        pwd = pwd.encode()
        hash_pwd = hashlib.sha1(pwd).hexdigest()
        result = {"username": name, "password": hash_pwd, "status_account": 1}

        with open("user_info.csv", 'a', newline='') as writer:
            csv_writer = csv.DictWriter(writer, fieldnames=["username", "password", "status_account"])
            csv_writer.writerow(result)
        return cls(name)

    @staticmethod
    def close_account(name):
        """
        change the value of status_account from 1 to 0
        :param name: name  of account to close
        """

        df = pd.read_csv("user_info.csv")
        df.loc[df["username"] == name] = df.loc[df["username"] == name].replace(1, 0)
        df.to_csv("user_info.csv", index=False)

    def log_in(self):
        """
        function for chek user login and return boolean
        :return: True if every thing is ok and false if the password is wrong after 3 times.
        """
        count = 0
        sentence = chek_pass(self.name)
        try:
            # chek status of account
            assert int(sentence[0]["status_account"])
            while count < 3:
                passwd = input("Please enter your password: ")
                passwd = passwd.encode()
                h = hashlib.sha1(passwd).hexdigest()
                # print(h)

                if sentence[0]["password"] == h:
                    return True
                else:
                    count += 1
                    print("Wrong Password in 3 times")
            print("Your account is closed")
            if self.name != 'admin':
                User.close_account(self.name)

        except AssertionError:
            # if self.name == 'admin':
            # active_account()
            # else:
            print("Your account is closed\nplease report this problem to admin")
            return False

    def change_password(self):
        """
        This function is changed the password of instance if the old password is OK.
        :return:True if the password is changed and false if is not.
        """
        df = pd.read_csv("user_info.csv")
        old_password = input("Please enter your old password")
        new_password = input("Please enter new password")
        old = hashlib.sha1(old_password.encode()).hexdigest()
        new = hashlib.sha1(new_password.encode()).hexdigest()
        if df.iloc[df.index[df['username'] == self.name].tolist()[0], 1] == old:
            df.loc[df["username"] == self.name] = df.loc[df["username"] == self.name].replace(old, new)
            df.to_csv("user_info.csv", index=False)
            return True
        else:
            print("wrong password")
            return False


class Customer(User):
    """
    The Customer class which inheritance of User class
    """

    @staticmethod
    def show_product():
        """
        This functions is for customer to see the products
        :return: pandas dataframe of products
        """
        df = pd.read_csv("Product_info.csv")
        print(df.loc[:, ["name", "price", "brand"]])
        return df

    @staticmethod
    def add_cards(df, prod, num):
        """
        This function add the product to the cards.
        :param df: dataframe of products
        :param prod: the id of products
        :param num: the number of products which customer need
        """
        cal_price = df.loc[prod, 'price'] * num
        df.loc[prod, 'quantity'] = df.loc[prod, 'quantity'] - num
        lst = df.loc[prod, ["name", "price"]]
        df2 = pd.DataFrame({"name": [lst[0]], "price": [lst[1]], "num": [num], "total": [cal_price]})
        print(df2)
        df2.to_csv('factor.csv', mode='a', index=False, sep=",", header=False)
        df.to_csv("Product_info.csv", index=False)

    @staticmethod
    def print_factor():
        """
        This function shows the products bought and the price of them and calculate total price.
        :return: factor of bought products
        """
        c_factor = pd.read_csv("factor.csv")
        df2 = pd.DataFrame(
            {"name": ["total"], "price": ["----"], "num": [sum(c_factor['num'])], "total": [sum(c_factor['total'])]})
        df2.to_csv('factor.csv', mode='a', index=False, sep=",", header=False)
        c_factor = pd.read_csv("factor.csv")
        print(c_factor)
        return c_factor

    @staticmethod
    def see_cards():
        """
        This function is show the bought products
        """
        c_factor = pd.read_csv("factor.csv")
        print(c_factor)

    @staticmethod
    def save_to_data(name, factor):
        """
        This function saves the factor to total_factors to admin
        :param name: name of user that is shopping
        :param factor: factor of bought products
        """
        data = {"name": [name], "action": [factor]}
        # data= factor
        data = pd.DataFrame(data)
        data.to_csv("total_factors.csv", mode='a', index=False, sep=",")
        # with open("total_factors.json", 'a') as f:
        #     json.dump(data, f)
        # print(factor)


class Admin(User):
    """
    The Admin class which inheritance of User class
    """
    str_sec = "_@ADMIN"
    hash_message = hashlib.sha1(str_sec.encode()).hexdigest()

    @staticmethod
    def verify_admin():
        """
        verify is it admin?
        """
        test_security = input("first setup\nplease enter the security sentence: ")
        test_security = test_security.encode()
        with open("security.json") as reader_file:
            if hashlib.sha1(test_security).hexdigest() == json.load(reader_file):
                return True
            else:
                print("wrong_input")
                return False

    @staticmethod
    def first_init():
        """
        create the user_info csv file and set the header.
        """
        with open("user_info.csv", 'a') as writer:
            csv_writer = csv.DictWriter(writer, fieldnames=["username", "password", "status_account"])
            csv_writer.writeheader()

    @staticmethod
    def show_product():
        """
        This functions is for admin to see the products.
        """
        df = pd.read_csv("Product_info.csv")
        print(df.loc[:, ["name", "price", "brand", "quantity"]])

    @staticmethod
    def create_product():
        """
        function for define  the product and save them to Product_info file.
        """
        df = pd.read_csv("Product_info.csv")
        while True:
            prod = input('Please enter the id,name,price,brand,quantity of products;\n enter e to exit: ').split(',')
            print(prod)
            if prod == ['e']:
                break

            prod = [int(x.strip()) if x.isdigit() else x for x in prod]
            if len(prod) == 5:
                if isinstance(prod[2], int) and isinstance(prod[4], int):
                    df2 = pd.Series(prod, index=["id", "name", "price", "brand", "quantity"])
                else:
                    print("Wrong input")
                    continue
            else:
                print("Wrong input")
                continue
            lst_id = list(df["id"])
            if prod[0] in lst_id:
                print("This product is exist. The price and the quantity is updated")
                id_row = df.index[df['id'] == prod[0]].tolist()[0]
                df.loc[id_row, "price"] = prod[2]
                df.loc[id_row, "quantity"] += prod[4]
            else:
                df = df.append(df2, ignore_index=True)
        df.to_csv("Product_info.csv", mode='w', index=False, sep=",", header=True)
        print(df.loc[:, ["name", "price", "brand", "quantity"]])

    @staticmethod
    def see_orders():
        """
        function to see the orders
        """
        data = pd.read_csv("total_factors.csv")
        print(data)
        # with open("total_factors.csv", 'r') as f:
        #     k=csv.reader(f)
        #     [print(row) for row in k]

    @staticmethod
    def active_account(name):
        """
        function for active close account
        :param name: the name of user that it's account is closed
        """
        df = pd.read_csv("user_info.csv")
        df.loc[df["username"] == name] = df.loc[df["username"] == name].replace(0, 1)
        df.to_csv("user_info.csv", index=False)


if __name__ == '__main__':
    # c=Admin('m')
    # Customer.add_cards(1, 2)
    # factor = pd.DataFrame({"name": [], "price": [], "num": [], "total": []})
    # factor.to_csv("factor.csv", index=False)
    # factor = pd.read_csv("factor.csv")
    # Customer.save_to_data('mah', factor)
    # Admin.see_orders()
    # pwd = input("Hi Admin,\n please set your password: ")
    admin = Admin('admin')
    admin.create_product()
