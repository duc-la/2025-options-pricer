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

            result_label.config(text=f"Call Price: {call_price:.2f}         Put Price: {put_price:.2f}")
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

    wrapper = tk.Frame(pricer_tab, padx=20, pady=20)
    wrapper.pack(fill='both', expand=True)

    left_col = tk.Frame(wrapper)
    left_col.pack(side='left', anchor = 'n', padx = 20, pady = 10)

    param_frame = tk.LabelFrame(left_col, text="Black Scholes Model Parameters", padx=15, pady=15)
    param_frame.pack( anchor='n', fill='x', expand=True)

    heatmap_frame = tk.LabelFrame(left_col, text="Heatmap Parameters", padx=30, pady=15)
    heatmap_frame.pack( anchor='n', fill='x', expand=True, pady=(20, 0))  

    pos_frame = tk.LabelFrame(wrapper, text="Call/Put Price", padx=30, pady=15)
    pos_frame.pack(side='left', anchor='n', padx=(40, 0))  

    
    tk.Label(param_frame, text="Stock Price (S):").grid(row=0, column=0)
    entry_S = tk.Entry(param_frame)
    entry_S.grid(row=0, column=1)

    tk.Label(param_frame, text="Strike Price (K):").grid(row=1, column=0)
    entry_K = tk.Entry(param_frame)
    entry_K.grid(row=1, column=1)

    tk.Label(param_frame, text="Time to Maturity (T):").grid(row=2, column=0)
    entry_T = tk.Entry(param_frame)
    entry_T.grid(row=2, column=1)

    tk.Label(param_frame, text="Volatility (σ):").grid(row=3, column=0)
    entry_sigma = tk.Entry(param_frame)
    entry_sigma.grid(row=3, column=1)

    tk.Label(param_frame, text="Risk-Free Rate (r):").grid(row=4, column=0)
    entry_r = tk.Entry(param_frame)
    entry_r.grid(row=4, column=1)


    tk.Label(heatmap_frame, text="Min Spot Price").grid(row=1, column=0)
    entry_min_spot = tk.Entry(heatmap_frame)
    entry_min_spot.grid(row=1, column=1)

    tk.Label(heatmap_frame, text="Max Spot Price").grid(row=2, column=0)
    entry_max_spot = tk.Entry(heatmap_frame)
    entry_max_spot.grid(row=2, column=1)

    tk.Label(heatmap_frame, text="Min Volatility").grid(row=1, column=0)
    entry_min_vol = tk.Entry(heatmap_frame)
    entry_min_vol.grid(row=1, column=1)

    tk.Label(heatmap_frame, text="Max Volatility").grid(row=2, column=0)
    entry_max_vol = tk.Entry(heatmap_frame)
    entry_max_vol.grid(row=2, column=1)

    tk.Button(param_frame, text="Calculate", command=calculate).grid(row=7, column=0, pady=10)
    tk.Button(param_frame, text="Upload CSV", command=upload_csv).grid(row=7, column=1)

    

    result_label = tk.Label(pos_frame, text="", font=("Helvetica", 12), justify="left")
    result_label.grid(row=1, column=2, rowspan=100, sticky='nw', padx=(20, 0))

    return pricer_tab
