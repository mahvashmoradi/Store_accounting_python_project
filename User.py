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
                    x['user'] == name]
        #print(sentence)
        return sentence


def close_account(name, hash_pwd):
    """
    change the value of status_account from 1 to 0
    :param name: name  of account to close
    :param hash_pwd: hash password
    """

    titanic = pd.read_csv("user_info.csv")
    print(titanic)
    titanic.loc[titanic["user"] == name] = titanic.loc[titanic["user"] == name].replace(1, 0)
    titanic.loc[:, ['user', 'password', 'status_account']].to_csv("user_info.csv")
    print(titanic)
    # dict1 = {"user": name, "password": hash_pwd, "status_account": 1}
    # dict2 = {"user": name, "password": hash_pwd, "status_account": 0}
    # with open("user_info.csv", "r") as rfh, open("user_info.csv", "a") as wfh:
    #      r = csv.DictReader(rfh)
    #      w = csv.DictWriter(wfh, fieldnames=["user", "password", "status_account"])
    #      [w.writerow(dict2) for x in r if x['user'] == name]
    #     for row in r:
    #         if row["user"] == name:
    #             print(row)
    #             w.writerow(dict2)
    # you can read using r and append using w


def active_account():
    print("Your account is active")


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
        The class method to create a user and write it on user_info.csv file
        :param name: name of user
        :param pwd: password of user
        :return: class
        """
        pwd = pwd.encode()
        hash_pwd = hashlib.sha1(pwd).hexdigest()
        result = {"user": name, "password": hash_pwd, "status_account": 1}

        with open("user_info.csv", 'a', newline='') as writer:
            csv_writer = csv.DictWriter(writer, fieldnames=["user", "password", "status_account"])
            # csv_writer.writeheader()
            csv_writer.writerow(result)
        return cls(name)

    def log_in(self):
        """
        function for chek user login and return boolean
        :return: boolean if every thing is ok
        """
        count = 0
        sentence = chek_pass(self.name)
        #print(sentence)
        try:
            # chek status of account
            assert int(sentence[0]["status_account"])
            while count < 3:
                passwd = input("enter your password")
                passwd = passwd.encode()
                h = hashlib.sha1(passwd).hexdigest()
                #print(h)

                if sentence[0]["password"] == h:
                    return True
                else:
                    count += 1
                    print("Wrong PassWord")
            print("Your account is closed")
            if self.name != 'admin':
                close_account(self.name, sentence[0]["password"])

        except AssertionError:
            if self.name == 'admin':
                active_account()
            else:
                print("Your account is closed\nplease report this problem to admin")
            return False

    @staticmethod
    def show_product():
        """
        This functions is for customer to see the products
        """
        print("see product")


class Customer(User):
    """
    The Customer class which inheritance of User class
    """

    def pay_buy(self):
        """
        function for calculate the bought
        """
        pass


class Admin(User):
    """
    The Admin class which inheritance of User class
    """
    str_sec = "_@ADMIN"

    global hash_message
    message = str_sec.encode()
    hash_message = hashlib.sha1(message).hexdigest()

    # message = str_sec.encode()
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
    def admin_init():
        """
        save admin information
        """
        with open("security.json", 'w') as write_file:
            json.dump(hash_message, write_file, ensure_ascii=False)
        with open("user_info.csv", 'w') as writer:
            csv_writer = csv.DictWriter(writer, fieldnames=["user", "password", "status_account"])
            csv_writer.writeheader()

    def create_product(self):
        """

        function for define  the product
        """
        pass

    def see_factor(self):
        """
        function to see the factors
        """
        pass

    def active_account(self):
        """

        function for active close account
        """
        pass


if __name__ == '__main__':
    close_account('ali','40bd001563085fc35165329ea1ff5c5ecbdbbeef')
    # c=Admin('m')
