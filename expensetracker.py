import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import locale

locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')

expenses = []

def load_expenses():
    try:
        with open('expenses.json', 'r') as file:
            global expenses
            expenses = json.load(file)
    except FileNotFoundError:
        pass

def save_expenses():
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file)

def add_expense():
    name = name_entry.get()
    amount = amount_entry.get()
    category = category_combobox.get()

    if not name or not amount or not category:
        messagebox.showerror("Input Error", "Please fill all fields!")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount should be a valid number!")
        return

    expense = {'name': name, 'amount': amount, 'category': category}
    expenses.append(expense)
    save_expenses()
    update_expenses_list()

    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def update_expenses_list():
    for row in tree.get_children():
        tree.delete(row)
    for idx, expense in enumerate(expenses):
        formatted_amount = locale.currency(expense['amount'], grouping=True)
        tag = 'even' if idx % 2 == 0 else 'odd'
        tree.insert("", "end", values=(expense['name'], formatted_amount, expense['category']), tags=(tag,))
    update_total_label()

def update_total_label():
    total = sum(expense['amount'] for expense in expenses)
    formatted_total = locale.currency(total, grouping=True)
    total_label.config(text=f"Total: {formatted_total}")

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

def total_expenses():
    total = sum(expense['amount'] for expense in expenses)
    formatted_total = locale.currency(total, grouping=True)
    messagebox.showinfo("Total Expenses", f"Total: {formatted_total}")

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

load_expenses()

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

label_font = ("Arial", 12)
entry_font = ("Helvetica", 12)

name_label = tk.Label(frame, text="Expense Name:", font=label_font, bg="#f0f0f0")
name_label.grid(row=0, column=0, padx=10, pady=5)

amount_label = tk.Label(frame, text="Amount:", font=label_font, bg="#f0f0f0")
amount_label.grid(row=1, column=0, padx=10, pady=5)

category_label = tk.Label(frame, text="Category:", font=label_font, bg="#f0f0f0")
category_label.grid(row=2, column=0, padx=10, pady=5)

name_entry = tk.Entry(frame, font=entry_font, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

amount_entry = tk.Entry(frame, font=entry_font, width=30)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

category_combobox = ttk.Combobox(frame, values=["Groceries", "Transport", "Entertainment", "Utilities", "Other"], font=entry_font, width=27)
category_combobox.grid(row=2, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Expense", width=15, command=add_expense, bg="#4CAF50", fg="white", font=("Arial", 14), relief="flat")
add_button.pack(pady=10)

tree = ttk.Treeview(root, columns=("Name", "Amount", "Category"), show="headings", height=10)
tree.heading("Name", text="Expense Name")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.column("Amount", width=100, anchor="center")
tree.column("Category", width=150)
tree.pack(pady=10, padx=20, fill="x")

tree.tag_configure('odd', background='#f9f9f9')
tree.tag_configure('even', background='#e8e8e8')

# Add total expense label beside delete button
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=5)

delete_button = tk.Button(button_frame, text="Delete Selected Expense", width=20, command=delete_expense, bg="#FF5733", fg="white", font=("Arial", 14), relief="flat")
delete_button.grid(row=0, column=0, padx=10)

total_label = tk.Label(button_frame, text="Total: ₹0.00", font=("Arial", 14), bg="#f0f0f0", fg="#333")
total_label.grid(row=0, column=1, padx=10)

total_button = tk.Button(root, text="Show Total Expenses", width=20, command=total_expenses, bg="#FF8C00", fg="white", font=("Arial", 14), relief="flat")
total_button.pack(pady=5)

update_expenses_list()
root.mainloop()
