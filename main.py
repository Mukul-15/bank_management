import mysql.connector as m
import getpass
from datetime import datetime

# Database connection
conn = m.connect(
    host="localhost",
    user="root",  
    password="Mysqlmukul@45",  
    database="bank_system"
)
cursor = conn.cursor()

# User Registration
def register():
    user_code = input("Enter a unique User Code: ")
    cursor.execute("SELECT * FROM users WHERE user_code = %s", (user_code,))
    
    if cursor.fetchone():
        print("User Code already exists! Try another one.")
        return

    name = input("Enter your name: ")
    password = getpass.getpass("Set your password: ")
    initial_balance = float(input("Enter initial deposit amount: "))

    cursor.execute("INSERT INTO users (user_code, name, password, balance) VALUES (%s, %s, %s, %s)", 
                   (user_code, name, password, initial_balance))
    conn.commit()

    print(f"Registration successful! Your User Code is: {user_code}")

# User Login
def login():
    user_code = input("Enter your User Code: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute("SELECT name FROM users WHERE user_code = %s AND password = %s", (user_code, password))
    user = cursor.fetchone()

    if user:
        print(f"Welcome, {user[0]}!")
        return user_code
    else:
        print("Invalid User Code or Password!")
        return None

# Forgot Password
def forgot_password():
    user_code = input("Enter your User Code: ")
    cursor.execute("SELECT * FROM users WHERE user_code = %s", (user_code,))
    
    if not cursor.fetchone():
        print("User not found!")
        return

    new_password = getpass.getpass("Enter new password: ")
    cursor.execute("UPDATE users SET password = %s WHERE user_code = %s", (new_password, user_code))
    conn.commit()
    print("Password reset successful!")

# Check Balance
def check_balance(user_code):
    cursor.execute("SELECT balance FROM users WHERE user_code = %s", (user_code,))
    balance = cursor.fetchone()[0]
    print(f"Your current balance: ₹{balance}")

# Send Money
def send_money(user_code):
    recipient_code = input("Enter recipient's User Code: ")
    
    cursor.execute("SELECT * FROM users WHERE user_code = %s", (recipient_code,))
    if not cursor.fetchone():
        print("Recipient not found!")
        return

    amount = float(input("Enter amount to send: "))

    cursor.execute("SELECT balance FROM users WHERE user_code = %s", (user_code,))
    sender_balance = cursor.fetchone()[0]

    if sender_balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_code = %s", (amount, user_code))
        cursor.execute("UPDATE users SET balance = balance + %s WHERE user_code = %s", (amount, recipient_code))
        
        # Log transaction
        cursor.execute("INSERT INTO transactions (user_code, type, amount) VALUES (%s, 'Sent', %s)", (user_code, amount))
        cursor.execute("INSERT INTO transactions (user_code, type, amount) VALUES (%s, 'Received', %s)", (recipient_code, amount))
        conn.commit()

        print(f"Sent ₹{amount} to {recipient_code}.")
    else:
        print("Insufficient balance!")

# Deposit Money
def deposit_money(user_code):
    amount = float(input("Enter amount to deposit: "))

    cursor.execute("UPDATE users SET balance = balance + %s WHERE user_code = %s", (amount, user_code))
    cursor.execute("INSERT INTO transactions (user_code, type, amount) VALUES (%s, 'Deposit', %s)", (user_code, amount))
    conn.commit()

    print(f"₹{amount} deposited successfully!")

# Withdraw Money
def withdraw_money(user_code):
    amount = float(input("Enter amount to withdraw: "))

    cursor.execute("SELECT balance FROM users WHERE user_code = %s", (user_code,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_code = %s", (amount, user_code))
        cursor.execute("INSERT INTO transactions (user_code, type, amount) VALUES (%s, 'Withdraw', %s)", (user_code, amount))
        conn.commit()
        print(f"₹{amount} withdrawn successfully!")
    else:
        print("Insufficient balance!")

# Transaction History
def transaction_history(user_code):
    cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE user_code = %s ORDER BY timestamp DESC", (user_code,))
    transactions = cursor.fetchall()

    print("\nTransaction History:")
    if transactions:
        for txn in transactions:
            print(f"{txn[0]} ₹{txn[1]} on {txn[2]}")
    else:
        print("No transactions yet.")

# Main Menu
def main():
    while True:
        print("\n-----BANK MANAGEMENT SYSTEM-----")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            user_code = login()
            if user_code:
                while True:
                    print("\n-----BANK MENU-----")
                    print("1. Check Balance")
                    print("2. Send Money")
                    print("3. Deposit Money")
                    print("4. Withdraw Money")
                    print("5. Transaction History")
                    print("6. Logout")

                    option = input("Choose an option: ")

                    if option == "1":
                        check_balance(user_code)
                    elif option == "2":
                        send_money(user_code)
                    elif option == "3":
                        deposit_money(user_code)
                    elif option == "4":
                        withdraw_money(user_code)
                    elif option == "5":
                        transaction_history(user_code)
                    elif option == "6":
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice!")
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            print("Exiting... Thank you!")
            conn.close()  # Close the database connection
            break
        else:
            print("Invalid option!")

# Run the app
if __name__ == "__main__":
    main()
