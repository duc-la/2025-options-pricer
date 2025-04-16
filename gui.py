import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from pricer import black_scholes

def launch_gui():
    def calculate():
        try:
            S = float(entry_S.get())
            K = float(entry_K.get())
            T = float(entry_T.get())
            r = float(entry_r.get())
            sigma = float(entry_sigma.get())

            call_price = black_scholes(S, K, T, r, sigma, "call")
            put_price = black_scholes(S, K, T, r, sigma, "put")

            result_label.config(text=f"Call Price: {call_price:.2f}\nPut Price: {put_price:.2f}")
        except Exception as e:
            messagebox.showerror("Input Error", str(e))

   
    # GUI Setup
    root = tk.Tk()
    root.title("Black-Scholes Options Pricer")

    tk.Label(root, text="Stock Price (S):").grid(row=0, column=0)
    entry_S = tk.Entry(root)
    entry_S.grid(row=0, column=1)

    tk.Label(root, text="Strike Price (K):").grid(row=1, column=0)
    entry_K = tk.Entry(root)
    entry_K.grid(row=1, column=1)

    tk.Label(root, text="Time to Maturity (T):").grid(row=2, column=0)
    entry_T = tk.Entry(root)
    entry_T.grid(row=2, column=1)

    tk.Label(root, text="Volatility (σ):").grid(row=3, column=0)
    entry_sigma = tk.Entry(root)
    entry_sigma.grid(row=3, column=1)

    tk.Label(root, text="Risk-Free Rate (r):").grid(row=4, column=0)
    entry_r = tk.Entry(root)
    entry_r.grid(row=4, column=1)


    tk.Button(root, text="Calculate", command=calculate).grid(row=5, column=0, pady=10)
    tk.Button(root, text="Upload CSV", command=upload_csv).grid(row=5, column=1)

    result_label = tk.Label(root, text="", font=("Helvetica", 12))
    result_label.grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()
