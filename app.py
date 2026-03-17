import streamlit as st
import re
from bank import Bank

Bank.load()

# Session State for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.account_no = None

menu = st.sidebar.selectbox("Menu", ["Home", "Create Account", "Login", "Logout", "Deposit", "Withdraw", "Transfer", "Transactions"])

if menu == "Home":
    st.title("Welcome to Python Bank")
    st.write("Please use the sidebar to navigate.")

# ------------------- CREATE ACCOUNT -------------------
elif menu == "Create Account":
    st.header("Create a New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password", max_chars=4)

    pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    valid_email = re.match(pattern, email)

    if st.button("Create Account"):
        if not all([name, age, email, pin]):
            st.error("All fields are required!")
        elif age < 18:
            st.error("You must be at least 18 years old.")
        elif not valid_email:
            st.error("Enter a valid Gmail address.")
        elif not (pin.isdigit() and len(pin) == 4):
            st.error("PIN must be exactly 4 digits.")
        else:
            account = Bank.create_account(name, age, email, pin)
            st.success(f"Account created! Your account number: {account['account_no']}")

# ------------------- LOGIN -------------------
elif menu == "Login":
    st.header("Login")
    if not st.session_state.logged_in:
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        if st.button("Login"):
            account = Bank.find_account(acc_no, pin)
            if account:
                st.session_state.logged_in = True
                st.session_state.account_no = acc_no
                st.success(f"Welcome {account['name']}!")
            else:
                st.error("Invalid account number or PIN")
    else:
        st.info("You are already logged in.")

# ------------------- LOGOUT -------------------
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.account_no = None
    st.success("Logged out successfully!")

# ------------------- DEPOSIT -------------------
elif menu == "Deposit":
    if st.session_state.logged_in:
        amount = st.number_input("Amount to Deposit", min_value=0.01)
        if st.button("Deposit"):
            acc = Bank.deposit(st.session_state.account_no, amount)
            st.success(f"Deposit successful! New balance: ${acc['balance']}")
    else:
        st.warning("Please login first.")

# ------------------- WITHDRAW -------------------
elif menu == "Withdraw":
    if st.session_state.logged_in:
        amount = st.number_input("Amount to Withdraw", min_value=0.01)
        if st.button("Withdraw"):
            acc = Bank.withdraw(st.session_state.account_no, amount)
            if acc:
                st.success(f"Withdrawal successful! New balance: ${acc['balance']}")
            else:
                st.error("Insufficient funds.")
    else:
        st.warning("Please login first.")

# ------------------- TRANSFER -------------------
elif menu == "Transfer":
    if st.session_state.logged_in:
        to_acc = st.text_input("Recipient Account Number")
        amount = st.number_input("Amount to Transfer", min_value=0.01)
        if st.button("Transfer"):
            success = Bank.transfer(st.session_state.account_no, to_acc, amount)
            if success:
                st.success("Transfer successful!")
            else:
                st.error("Transfer failed. Check account numbers or balance.")
    else:
        st.warning("Please login first.")

# ------------------- TRANSACTIONS -------------------
elif menu == "Transactions":
    if st.session_state.logged_in:
        acc = Bank.find_account(st.session_state.account_no)
        st.header("Transaction History")
        if acc["transactions"]:
            for tx in acc["transactions"]:
                st.write(tx)
        else:
            st.info("No transactions yet.")
    else:
        st.warning("Please login first.")