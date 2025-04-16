import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from models.pricer import black_scholes

def launch_gui(notebook):
    

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

    def upload_csv():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                output = ""
                for i, row in enumerate(reader, 1):
                    S = float(row['S'])
                    K = float(row['K'])
                    T = float(row['T'])
                    r = float(row['r'])
                    sigma = float(row['sigma'])

                    call = black_scholes(S, K, T, r, sigma)
                    put = black_scholes(S, K, T, r, sigma)

                    output += f"Row {i}: Call = {call:.2f}, Put = {put:.2f}\n"

                messagebox.showinfo("Results", output)
        except Exception as e:
            messagebox.showerror("CSV Error", str(e))

     # GUI Setup
    pricer_tab = tk.Frame(notebook)
    notebook.add(pricer_tab, text="Options Pricer")
    
    #pricer_tab.title("Black-Scholes Options Pricer")

    tk.Label(pricer_tab, text="Stock Price (S):").grid(row=0, column=0)
    entry_S = tk.Entry(pricer_tab)
    entry_S.grid(row=0, column=1)

    tk.Label(pricer_tab, text="Strike Price (K):").grid(row=1, column=0)
    entry_K = tk.Entry(pricer_tab)
    entry_K.grid(row=1, column=1)

    tk.Label(pricer_tab, text="Time to Maturity (T):").grid(row=2, column=0)
    entry_T = tk.Entry(pricer_tab)
    entry_T.grid(row=2, column=1)

    tk.Label(pricer_tab, text="Volatility (σ):").grid(row=3, column=0)
    entry_sigma = tk.Entry(pricer_tab)
    entry_sigma.grid(row=3, column=1)

    tk.Label(pricer_tab, text="Risk-Free Rate (r):").grid(row=4, column=0)
    entry_r = tk.Entry(pricer_tab)
    entry_r.grid(row=4, column=1)


    tk.Button(pricer_tab, text="Calculate", command=calculate).grid(row=5, column=0, pady=10)
    tk.Button(pricer_tab, text="Upload CSV", command=upload_csv).grid(row=5, column=1)

    result_label = tk.Label(pricer_tab, text="", font=("Helvetica", 12))
    result_label.grid(row=1, column=3, columnspan=2, pady=10)

    return pricer_tab
