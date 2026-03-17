import json
import os
import hashlib
from datetime import datetime

class Bank:
    data_file = "data.bank.json"
    data = []

    @staticmethod
    def load():
        if os.path.exists(Bank.data_file):
            try:
                with open(Bank.data_file, "r") as f:
                    Bank.data = json.load(f)
            except:
                Bank.data = []


    @staticmethod
    def save():
        with open(Bank.data_file, "w") as f:
            json.dump(Bank.data, f, indent=4)

    @staticmethod
    def hash_pin(pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    @staticmethod
    def generate_account_no():
        if Bank.data:
            last_acc = Bank.data[-1]["account_no"]
            return str(int(last_acc)+1)
        return "100000001"
    
    @classmethod
    def create_account(cls, name, age, email, pin):
        account = {
            "account_no" : cls.generate_account_no(),
            "name": name,
            "age": age,
            "email": email,
            "pin": cls.hash_pin(pin),
            "balance": 0,
            "transactions": []
        }

        cls.data.append(account)
        cls.save()
        return account
    
    @classmethod
    def find_account(cls, account_no,pin=None):
        for account in cls.data:
            if account["account_no"] == account_no:
                if pin is None or account["pin"] == cls.hash_pin(pin):
                    return account
        return None
    
    @classmethod
    def authenticate(cls, account_no, pin):
        account = cls.find_account(account_no, pin)
        if account:
            return account
        return None
    
    @classmethod
    def deposit(cls, account_no, amount):
        acc = cls.find_account(account_no)
        if acc:
            acc["balance"] += amount
            acc["transactions"].append({"Type": "Deposit", "Amount": amount, "Date": str(datetime.now())})
            cls.save()
            return acc
        return None
    
    @classmethod
    def withdraw(cls, account_no, amount):
        acc = cls.find_account(account_no)
        if acc and acc["balance"] >= amount:
            acc["balance"] -= amount
            acc["transactions"].append({"Type": "Withdrawal", "Amount": amount, "Date": str(datetime.now())})
            cls.save()
            return acc
        return None
    
    @classmethod
    def transfer(cls, from_acc_no, to_acc_no, amount):
        from_acc = cls.find_account(from_acc_no)
        to_acc = cls.find_account(to_acc_no)
        if from_acc and to_acc and from_acc["balance"] >= amount:
            from_acc["balance"]-= amount
            to_acc["balance"] += amount

            from_acc["transactions"].append({"Type": "Transfer Out", "Amount": amount, "Date": str(datetime.now()), "To": to_acc_no})
            to_acc["transactions"].append({"Type": "Transfer In", "Amount": amount, "Date": str(datetime.now()), "From": from_acc_no})

            cls.save()
            return from_acc
        return None