import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

# Initialize list to store expenses
expenses = []

# Load expenses from file (if exists)
def load_expenses():
    try:
        with open('expenses.json', 'r') as file:
            global expenses
            expenses = json.load(file)
    except FileNotFoundError:
        pass  # If file doesn't exist, we start with an empty list

# Save expenses to file
def save_expenses():
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file)

# Add an expense
def add_expense():
    name = name_entry.get()
    amount = amount_entry.get()
    category = category_combobox.get()

    # Validate input
    if not name or not amount or not category:
        messagebox.showerror("Input Error", "Please fill all fields!")
        return
    try:
        amount = float(amount)  # Ensure the amount is a number
    except ValueError:
        messagebox.showerror("Input Error", "Amount should be a valid number!")
        return

    # Add the expense to the list
    expense = {'name': name, 'amount': amount, 'category': category}
    expenses.append(expense)
    save_expenses()
    update_expenses_list()

    # Clear the input fields
    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Update the expense list in the GUI
def update_expenses_list():
    for row in tree.get_children():
        tree.delete(row)  # Clear the treeview
    for expense in expenses:
        tree.insert("", "end", values=(expense['name'], f"${expense['amount']:.2f}", expense['category']))

# Delete an expense
def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Delete Error", "Please select an expense to delete.")
        return
    expense_name = tree.item(selected_item, 'values')[0]
    global expenses
    expenses = [expense for expense in expenses if expense['name'] != expense_name]
    save_expenses()
    update_expenses_list()

# Show total expenses
def total_expenses():
    total = sum(expense['amount'] for expense in expenses)
    messagebox.showinfo("Total Expenses", f"Total: ${total:.2f}")

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")
root.configure(bg="#f0f0f0")  # Light background color

# Load existing expenses from file
load_expenses()

# Create a frame for input fields and buttons
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

# Custom Fonts
label_font = ("Arial", 12)
entry_font = ("Helvetica", 12)

# Labels for input fields
name_label = tk.Label(frame, text="Expense Name:", font=label_font, bg="#f0f0f0")
name_label.grid(row=0, column=0, padx=10, pady=5)

amount_label = tk.Label(frame, text="Amount:", font=label_font, bg="#f0f0f0")
amount_label.grid(row=1, column=0, padx=10, pady=5)

category_label = tk.Label(frame, text="Category:", font=label_font, bg="#f0f0f0")
category_label.grid(row=2, column=0, padx=10, pady=5)

# Input fields
name_entry = tk.Entry(frame, font=entry_font, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

amount_entry = tk.Entry(frame, font=entry_font, width=30)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

category_combobox = ttk.Combobox(frame, values=["Groceries", "Transport", "Entertainment", "Utilities", "Other"], font=entry_font, width=27)
category_combobox.grid(row=2, column=1, padx=10, pady=5)

# Add Expense Button (styled with a background color)
add_button = tk.Button(root, text="Add Expense", width=15, command=add_expense, bg="#4CAF50", fg="white", font=("Arial", 14), relief="flat")
add_button.pack(pady=10)

# Create a Treeview widget for displaying expenses (styled with a custom background)
tree = ttk.Treeview(root, columns=("Name", "Amount", "Category"), show="headings", height=10)
tree.heading("Name", text="Expense Name")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.column("Amount", width=100, anchor="center")
tree.column("Category", width=150)
tree.pack(pady=10, padx=20, fill="x")

# Treeview styling: Alternate row colors
tree.tag_configure('odd', background='#f9f9f9')
tree.tag_configure('even', background='#e8e8e8')

# Buttons for delete and total expenses
delete_button = tk.Button(root, text="Delete Selected Expense", width=20, command=delete_expense, bg="#FF5733", fg="white", font=("Arial", 14), relief="flat")
delete_button.pack(pady=5)

total_button = tk.Button(root, text="Total Expenses", width=20, command=total_expenses, bg="#FF8C00", fg="white", font=("Arial", 14), relief="flat")
total_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
