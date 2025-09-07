import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Main Window ----------------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x600")
root.config(bg="white")

expenses = []  # List to store all expenses

# ---------------- Functions ----------------
def add_expense():
    desc = desc_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()

    if not desc or not category or not amount:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    expenses.append((desc, category, amount))
    update_expense_list()
    update_total()
    update_category_filter()

    # Clear input fields
    desc_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an expense to delete.")
        return

    index = int(tree.item(selected_item, "values")[0]) - 1  # Get index from serial number
    del expenses[index]

    update_expense_list()
    update_total()
    update_category_filter()

def update_expense_list(filtered=None):
    for row in tree.get_children():
        tree.delete(row)

    data = filtered if filtered is not None else expenses

    for i, (desc, category, amount) in enumerate(data, start=1):
        tree.insert("", "end", values=(i, desc, category, f"${amount:.2f}"))

def update_total(filtered=None):
    data = filtered if filtered is not None else expenses
    total = sum(amount for _, _, amount in data)
    total_label.config(text=f"Total: ${total:.2f}")

def update_category_filter():
    categories = sorted(set(cat for _, cat, _ in expenses))
    category_filter["values"] = ["All"] + categories
    if "All" not in category_filter.get():
        category_filter.current(0)

def apply_filter():
    selected = category_filter.get()
    if selected == "All":
        update_expense_list()
        update_total()
    else:
        filtered = [exp for exp in expenses if exp[1] == selected]
        update_expense_list(filtered)
        update_total(filtered)

def apply_sort():
    key = sort_by.get()
    order = sort_order.get()

    if not expenses:
        return

    reverse = (order == "Descending")

    if key == "Description":
        sorted_data = sorted(expenses, key=lambda x: x[0].lower(), reverse=reverse)
    elif key == "Category":
        sorted_data = sorted(expenses, key=lambda x: x[1].lower(), reverse=reverse)
    elif key == "Amount":
        sorted_data = sorted(expenses, key=lambda x: x[2], reverse=reverse)
    else:
        sorted_data = expenses

    update_expense_list(sorted_data)
    update_total(sorted_data)

# ---------------- UI Elements ----------------
# Input Fields
tk.Label(root, text="Description", bg="white").pack()
desc_entry = tk.Entry(root, width=40)
desc_entry.pack()

tk.Label(root, text="Category", bg="white").pack()
category_entry = tk.Entry(root, width=40)
category_entry.pack()

tk.Label(root, text="Amount ($)", bg="white").pack()
amount_entry = tk.Entry(root, width=40)
amount_entry.pack()

# Buttons
btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white", width=15)
add_btn.grid(row=0, column=0, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Expense", command=delete_expense, bg="#F44336", fg="white", width=15)
delete_btn.grid(row=0, column=1, padx=5)

# Filter & Sort Controls
filter_frame = tk.LabelFrame(root, text="Filter & Sort", bg="white", padx=10, pady=10)
filter_frame.pack(pady=10, fill="x")

tk.Label(filter_frame, text="Filter by Category:", bg="white").grid(row=0, column=0, sticky="w")
category_filter = ttk.Combobox(filter_frame, values=["All"], state="readonly", width=15)
category_filter.current(0)
category_filter.grid(row=0, column=1, padx=5)
tk.Button(filter_frame, text="Apply Filter", command=apply_filter, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)

tk.Label(filter_frame, text="Sort by:", bg="white").grid(row=1, column=0, sticky="w")
sort_by = ttk.Combobox(filter_frame, values=["Description", "Category", "Amount"], state="readonly", width=15)
sort_by.current(0)
sort_by.grid(row=1, column=1, padx=5)

sort_order = ttk.Combobox(filter_frame, values=["Ascending", "Descending"], state="readonly", width=15)
sort_order.current(0)
sort_order.grid(row=1, column=2, padx=5)

tk.Button(filter_frame, text="Apply Sort", command=apply_sort, bg="#9C27B0", fg="white").grid(row=1, column=3, padx=5)

# Expense Table
columns = ("#", "Description", "Category", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(pady=10, fill="x")

# Total Label
total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 12, "bold"), bg="white", fg="green")
total_label.pack(pady=10)

# Run App
root.mainloop()
