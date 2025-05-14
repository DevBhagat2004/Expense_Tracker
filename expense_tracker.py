import sqlite3
import hashlib
import matplotlib.pyplot as plt
import pandas as pd

# Connect to SQLite Database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create User Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Create Expenses Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    category TEXT,
    description TEXT,
    amount REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
conn.commit()

# Hashing Passwords for Security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register New User
def register():
    username = input("Enter a new username: ")
    password = input("Enter a password: ")
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, hash_password(password)))
    conn.commit()
    print("User registered successfully.")

# Login User
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                   (username, hash_password(password)))
    user = cursor.fetchone()

    if user:
        print("Login successful.")
        user_menu(user[0])
    else:
        print("Invalid username or password.")

# User Menu after Login
def user_menu(user_id):
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Visualize Expenses")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(user_id)
        elif choice == "2":
            view_expenses(user_id)
        elif choice == "3":
            visualize_expenses(user_id)
        elif choice == "4":
            print("Logged out.")
            break
        else:
            print("Invalid choice. Please try again.")

# Add an Expense
def add_expense(user_id):
    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the category (e.g., Food, Transport, Utilities): ")
    description = input("Enter the description: ")
    amount = float(input("Enter the amount: "))

    cursor.execute("""
    INSERT INTO expenses (user_id, date, category, description, amount)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, category, description, amount))
    conn.commit()
    print("Expense added successfully.")

# View Expenses
def view_expenses(user_id):
    cursor.execute("SELECT date, category, description, amount FROM expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()

    if expenses:
        print("\nYour Expenses:")
        for exp in expenses:
            print(f"Date: {exp[0]}, Category: {exp[1]}, Description: {exp[2]}, Amount: ${exp[3]}")
    else:
        print("No expenses recorded.")

# Visualize Expenses with Bar Chart
def visualize_expenses(user_id):
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category", (user_id,))
    data = cursor.fetchall()

    if data:
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.bar(categories, amounts)
        plt.title("Expense by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.show()
    else:
        print("No expenses to visualize.")

# Main Program Loop
def main():
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    conn.close()
