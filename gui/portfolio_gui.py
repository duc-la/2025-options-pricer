import tkinter as tk
from tkinter import ttk

def launch_portfolio_tab(parent_frame):
    label = ttk.Label(parent_frame, text="Current Positions", font=("Arial", 16))
    label.pack(pady=10)

    header_frame = tk.Frame(parent_frame)
    header_frame.pack()

    fields = ["Symbol", "Type", "Strike", "Exp.", "Qty", "Entry", "Est. Price", "Act. Price", "PnL"]
    for i, field in enumerate(fields):
        tk.Label(header_frame, text=field, font=("Arial", 10, "bold"), padx=5).grid(row=0, column=i)

    entry_container = tk.Frame(parent_frame)
    entry_container.pack()

    position_rows = []

    def add_row(default_data=None):
        row = []
        default_data = default_data or ["", "Call", "", "", "", "", "", "", ""]
        idx = len(position_rows)

        for i, value in enumerate(default_data):
            if fields[i] == "Type":
                combo = ttk.Combobox(entry_container, values=["Call", "Put"], width=6)
                combo.set(value)
                combo.grid(row=idx, column=i, padx=5, pady=2)
                row.append(combo)
            else:
                entry = tk.Entry(entry_container, width=10)
                entry.insert(0, value)
                entry.grid(row=idx, column=i, padx=5, pady=2)
                row.append(entry)

        position_rows.append(row)

    def get_positions():
        return [[cell.get() for cell in row] for row in position_rows]

    # Add a sample row
    add_row(["AAPL", "Call", "150", "2025-06-21", "10", "3.2", "4.1", "4.25", "+32%"])

    add_btn = tk.Button(parent_frame, text="+ Add New Position", command=add_row)
    add_btn.pack(pady=10)

    # Optional: expose `get_positions()` later for data sharing
    parent_frame.get_positions = get_positions