import json
import csv
import pandas as pd
import hashlib


class User:
    """
    The class User which have 2 child class(Admin and Customer)
    """

    def __init__(self, name):
        """
        init of User class
        :param name: name of user
        """
        self.name = name

    def chek_pass(self, passwd, df):
        """
        This function gives the password of user and dataframe of user info and return the boolean
        :param df: dataframe of user info
        :param passwd: input password to chek
        :return: True if password is correct and false if is not
        """
        if list(df.loc[df["username"] == self.name, "password"])[0] == hashlib.sha1(passwd.encode()).hexdigest():
            return True
        else:
            return False

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
    def close_account(df, name):
        """
        change the value of status_account from 1 to 0
        :param df: dataframe of user info
        :param name: name  of account to close
        """
        df.loc[df["username"] == name] = df.loc[df["username"] == name].replace(1, 0)
        df.to_csv("user_info.csv", index=False)

    def change_password(self, df, old_password, new_password):
        """
        This function is changed the password of instance if the old password is OK.
        :param new_password: new password of user
        :param old_password: old password of user
        :param df: dataframe of user info
        :return:True if the password is changed and false if is not.
        """
        old = hashlib.sha1(old_password.encode()).hexdigest()
        new = hashlib.sha1(new_password.encode()).hexdigest()
        if df.iloc[df.index[df['username'] == self.name].tolist()[0], 1] == old:
            df.loc[df["username"] == self.name] = df.loc[df["username"] == self.name].replace(old, new)
            df.to_csv("user_info.csv", index=False)
            return "Your password is changed"
        else:
            return "wrong password\nYour password is not changed"


class Customer(User):
    """
    The Customer class which inheritance of User class
    """

    @staticmethod
    def show_product(df):
        """
        This functions is for customer to see the products
        :return: pandas dataframe of products
        """
        return df.loc[:, ["name", "price", "brand"]]

    @staticmethod
    def chek_quantity(df, prod, num):
        """
        This function chek the quantity of product
        :param df: dataframe of products
        :param prod: the id of products
        :param num: the number of products which customer need
        :return: the status of added product
        """
        amount = df.loc[prod, 'quantity'] - num
        if amount < 0:
            remain = df.loc[prod, 'quantity']
            if remain != 0:
                return [False, f"Sorry, There is not enough supply\nThere is just {remain}"]
            else:
                return [False, f"Sorry, This product is finished. It will be replaced as soon"]
        else:
            return [True, "The product is added to your cards"]

    @staticmethod
    def add_cards(df, df2, prod, num, logger):
        """
        This function add the product to the cards.
        :param df: dataframe of products
        :param df2: dataframe of factors
        :param prod: the id of products
        :param num: the number of products which customer need
        :param logger: logger to set the log
        :return: the status of added product
        """
        amount = df.loc[prod, 'quantity'] - num
        if amount == 0:
            logger.warning(f"{df.loc[prod, 'name']} with id {df.loc[prod, 'id']} is finished")
        cal_price = int(df.loc[prod, 'price'] * num)
        df.loc[prod, 'quantity'] = amount
        lst = df.loc[prod, ["name", "price"]]
        df3 = pd.DataFrame({"name": [lst[0]], "price": [lst[1]], "num": [num], "total": [cal_price]})
        # df2.to_csv('factor.csv', mode='a', index=False, sep=",", header=False)
        print(df3)
        # print(df2)
        df2 = df2.append(df3, ignore_index=True)
        return df, df2

    @staticmethod
    def print_factor(factor):
        """
        This function shows the products bought and the price of them and calculate total price.
        :return: factor of bought products
        """
        df2 = pd.DataFrame(
            {"name": ["total"], "price": ["----"], "num": [sum(factor['num'])], "total": [sum(factor['total'])]})
        factor = factor.append(df2, ignore_index=True)
        #df2.to_csv('factor.csv', mode='a', index=False, sep=",", header=False)
        return factor

    @staticmethod
    def see_cards(factor):
        """
        This function is show the bought products
        :param factor: dataframe of factor
        """
        df2 = pd.DataFrame(
            {"name": ["total"], "price": ["----"], "num": [sum(factor['num'])], "total": [sum(factor['total'])]})
        factor = factor.append(df2, ignore_index=True)
        return factor

    @staticmethod
    def save_to_data(name, factor):
        """
        This function saves the factor to total_factors to admin
        :param name: name of user that is shopping
        :param factor: factor of bought products
        """
        with open("total_factors.txt", 'a') as f:
            f.write(f"customer_name: {name}\n")
            f.writelines(f"{factor}")
            f.write("\n")
            f.write("----------------------------------------------------------\n")


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
    def show_product(df):
        """
        This functions is for admin to see the products.
        :param df: Product Dataframe panda
        """
        print(df.loc[:, ["name", "price", "brand", "quantity"]])

    @staticmethod
    def show_finished_product(df):
        """
        This functions is for admin to see the finished products.
        :param df: Product Dataframe panda
        """
        df2 = df.loc[df["quantity"] == 0]
        print(df2.loc[:, ["name", "price", "brand", "quantity"]])
        # print(df.loc[:, ["name", "price", "brand", "quantity"]])

    @staticmethod
    def create_product(df, prod):
        """
        function for define the product and save them to Product_info file.
        :param df: Product Dataframe panda
        :param prod: the information of product to add
        :return: the dataframe of products with new product
        """
        df2 = pd.Series(prod, index=["id", "name", "price", "brand", "quantity"])
        lst_id = list(df["id"])
        if prod[0] in lst_id:
            print("This product is exist.")
            id_row = df.index[df['id'] == prod[0]].tolist()[0]
            if df.loc[id_row, "name"] == prod[1]:
                df.loc[id_row, "price"] = prod[2]
                df.loc[id_row, "quantity"] += prod[4]
                print("The price and the quantity is updated")
            else:
                print("same id but different name\nPlease chek")
        else:
            df = df.append(df2, ignore_index=True)
        return df

    @staticmethod
    def see_orders():
        """
        function to see the orders
        """
        with open("total_factors.txt", 'r') as f:
            print(f.read())

    @staticmethod
    def active_account(df, name):
        """
        function for active close account
        :param df: dataframe of user info
        :param name: the name of user that it's account is closed
        """
        df.loc[df["username"] == name] = df.loc[df["username"] == name].replace(0, 1)
        df.to_csv("user_info.csv", index=False)


if __name__ == '__main__':
    pass
    # c=Admin('m')
    # Customer.add_cards(1, 2)
    # factor = pd.DataFrame({"name": [], "price": [], "num": [], "total": []})
    # factor.to_csv("factor.csv", index=False)
    # factor = pd.read_csv("Product_info.csv")
    # Customer.save_to_data('mah', factor)
    # Admin.see_orders()
    # print(list(df.loc[df["username"] == "admin"])[1])
    # Admin.show_finished_product(factor)
