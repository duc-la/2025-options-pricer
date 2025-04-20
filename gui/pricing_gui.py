import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from models.pricer import black_scholes

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#from gui.portfolio_gui import update_positions

#TODO: Finalize documentation at the end
def launch_gui(notebook):
    #Function for displaying options prices
    def calculate():
        try:
            S = float(entry_S.get())
            K = float(entry_K.get())
            T = float(entry_T.get())
            r = float(entry_r.get())
            sigma = float(entry_sigma.get())

            call_price = black_scholes(S, K, T, r, sigma, "call")
            put_price = black_scholes(S, K, T, r, sigma, "put")


            call_label.config(text=f"Call Price: {call_price:.2f}")
            put_label.config(text=f"Put Price: {put_price:.2f}")
            #result_label.config(text=f"Call Price: {call_price:.2f}         Put Price: {put_price:.2f}")
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

    #Function for heatmap
    def display_custom_heatmap(frame, option_type='call'):
        # Create grid of option prices
        vol1 = float( entry_min_vol.get() )
        vol2 = float( entry_max_vol.get() )
        vol_inc = int( entry_inc_vol.get() )

        spot1 = float( entry_min_spot.get() )
        spot2 = float( entry_max_spot.get() )
        spot_inc = int( entry_inc_spot.get() )

        S = float(entry_S.get())
        K = float(entry_K.get())
        T = float(entry_T.get())
        r = float(entry_r.get())
        sigma = float(entry_sigma.get())

        spot_range = np.linspace(spot1, spot2, spot_inc)
        vol_range = np.linspace(vol1, vol2, vol_inc)

        call_prices = np.zeros((len(vol_range), len(spot_range)))
        put_prices = np.zeros((len(vol_range), len(spot_range)))


        #Put prices into np array for later 
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                call_price = black_scholes(spot, K, T, r, vol)
                put_price = black_scholes(spot, K, T, r, vol, "put")
                
                call_prices[i, j] = call_price
                put_prices[i, j] = put_price


            
        # Create the heatmap for calls
        if option_type == "call":
            base_call_price = black_scholes(S, K, T, r, sigma, option_type)
            call_annot = np.empty_like(call_prices, dtype=object)
            for i in range(call_prices.shape[0]):
                for j in range(call_prices.shape[1]):
                    price = call_prices[i, j]
                    percent = (call_prices[i, j] - base_call_price) / base_call_price * 100
                    call_annot[i, j] = f"{price:.2f}\n({int(percent):+d}%)"

            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                        annot=call_annot, fmt="", cmap="RdYlGn", ax=ax)
            
            ax.set_title(f"{option_type.capitalize()} Price Heatmap")
            ax.set_xlabel("Spot Price")
            ax.set_ylabel("Volatility")
        
        #Create the heatmap for puts
        else:
            base_put_price = black_scholes(S, K, T, r, sigma, option_type)
            put_annot = np.empty_like(put_prices, dtype=object)
            for i in range(put_prices.shape[0]):
                for j in range(put_prices.shape[1]):
                    price = put_prices[i, j]
                    percent = (put_prices[i, j] - base_put_price) / base_put_price * 100
                    put_annot[i, j] = f"{price:.2f}\n({int(percent):+d}%)"

            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                        annot=put_annot, fmt="", cmap="RdYlGn", ax=ax)
            
            ax.set_title(f"{option_type.capitalize()} Price Heatmap")
            ax.set_xlabel("Spot Price")
            ax.set_ylabel("Volatility")

        # Clear any previous plot widgets in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Embed in tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Close to prevent matplotlib from launching window
        plt.close(fig)
    
    def get_current_option_data(option_type):
        return {
            "ticker" : entry_ticker.get(),
            "option_type": option_type,
            "S": float(entry_S.get()),
            "K": float(entry_K.get()),
            "T": float(entry_T.get()),
            "r": float(entry_r.get()),
            "sigma": float(entry_sigma.get())
        }

    # GUI Setup
    pricer_tab = tk.Frame(notebook)
    notebook.add(pricer_tab, text="Options Pricer")
    
    #pricer_tab.title("Black-Scholes Options Pricer")

    wrapper = tk.Frame(pricer_tab, padx=20, pady=20)
    wrapper.pack(fill='both', expand=True)

    #Left column
    left_col = tk.Frame(wrapper)
    left_col.pack(side='left', anchor = 'n', padx = 20, pady = 10)

    param_frame = tk.LabelFrame(left_col, text="Black Scholes Model Parameters", padx=15, pady=15)
    param_frame.pack( anchor='n', fill='x', expand=True)

    heatmap_frame = tk.LabelFrame(left_col, text="Heatmap Parameters", padx=30, pady=15)
    heatmap_frame.pack( anchor='n', fill='x', expand=True, pady=(20, 0))  

    #Right column
    right_col = tk.Frame(wrapper)
    right_col.pack(side='left', anchor='n', padx=(40, 0), pady=10)

    pos_frame = tk.LabelFrame(right_col, text="Call/Put Price", padx=30, pady=15)
    pos_frame.pack(anchor='n', fill='x')

    heatmap_plot = tk.LabelFrame(right_col, text="Heatmap Plot", padx=30, pady=15)
    heatmap_plot.pack(anchor='n', fill='both', expand=True, pady=(20, 0))


    #Black Scholes Frame stuff    
    tk.Label(param_frame, text="Current Ticker Symbol:").grid(row=0, column=0)
    entry_ticker = tk.Entry(param_frame)
    entry_ticker.grid(row=0, column=1)
    entry_ticker.insert(0, "XYZ")

    tk.Label(param_frame, text="Stock Price (S):").grid(row=1, column=0)
    entry_S = tk.Entry(param_frame)
    entry_S.grid(row=1, column=1)
    entry_S.insert(0, "100")

    tk.Label(param_frame, text="Strike Price (K):").grid(row=2, column=0)
    entry_K = tk.Entry(param_frame)
    entry_K.grid(row=2, column=1)
    entry_K.insert(0, "100")

    tk.Label(param_frame, text="Time to Maturity (T):").grid(row=3, column=0)
    entry_T = tk.Entry(param_frame)
    entry_T.grid(row=3, column=1)
    entry_T.insert(0, "1")

    tk.Label(param_frame, text="Volatility (σ):").grid(row=4, column=0)
    entry_sigma = tk.Entry(param_frame)
    entry_sigma.grid(row=4, column=1)
    entry_sigma.insert(0, "0.2")


    tk.Label(param_frame, text="Risk-Free Rate (r):").grid(row=5, column=0)
    entry_r = tk.Entry(param_frame)
    entry_r.grid(row=5, column=1)
    entry_r.insert(0, "0.05")

    tk.Button(param_frame, text="Calculate", command=calculate).grid(row=7, column=0, pady=10)
    tk.Button(param_frame, text="Upload CSV", command=upload_csv).grid(row=7, column=1)

    #Heatmap frame stuff
    tk.Label(heatmap_frame, text="Min Spot Price").grid(row=1, column=0)
    entry_min_spot = tk.Entry(heatmap_frame)
    entry_min_spot.grid(row=1, column=1)
    entry_min_spot.insert(0, "80")

    tk.Label(heatmap_frame, text="Max Spot Price").grid(row=2, column=0)
    entry_max_spot = tk.Entry(heatmap_frame)
    entry_max_spot.grid(row=2, column=1)
    entry_max_spot.insert(0, "120")

    tk.Label(heatmap_frame, text="Number of Spot Price Columns").grid(row=3, column=0, )
    entry_inc_spot = tk.Entry(heatmap_frame)
    entry_inc_spot.grid(row=3, column=1, )
    entry_inc_spot.insert(0, "10")


    tk.Label(heatmap_frame, text="Min Volatility").grid(row=4, column=0, pady=(10, 0))
    entry_min_vol = tk.Entry(heatmap_frame)
    entry_min_vol.grid(row=4, column=1, pady=(10, 0))
    entry_min_vol.insert(0, "0.1")

    tk.Label(heatmap_frame, text="Max Volatility").grid(row=5, column=0)
    entry_max_vol = tk.Entry(heatmap_frame)
    entry_max_vol.grid(row=5, column=1)
    entry_max_vol.insert(0, "0.3")

    tk.Label(heatmap_frame, text="Number of Volatility Rows").grid(row=6, column=0)
    entry_inc_vol = tk.Entry(heatmap_frame)
    entry_inc_vol.grid(row=6, column=1)
    entry_inc_vol.insert(0, "10")

    #Heatmap activation stuff
    tk.Button(
    heatmap_frame,
    text="Call Heatmap",
    command=lambda: display_custom_heatmap( heatmap_plot, option_type='call')
    ).grid(row=7, column=0, columnspan=2, pady=10)

    tk.Button(
    heatmap_frame,
    text="Put Heatmap",
    command=lambda: display_custom_heatmap( heatmap_plot, option_type='put')
    ).grid(row=7, column=1, pady=10)

    #Position Frame stuff
    call_label = tk.Label(pos_frame, text="Call Price: -", font=("Helvetica", 12), anchor="w")
    call_label.grid(row=1, column=0, sticky='w', padx=5, pady=(10, 5))

    # tk.Button(pos_frame, text="Update Call Positions in Portfolio Tab", 
    #       command=lambda: update_positions(get_current_option_data("call")))\
    #       .grid(row=1, column=1, pady=10)
    #tk.Button(pos_frame, text="Add/Update Call Position").grid(row=1, column=1, sticky='w', padx=10, pady=(10, 5))

    put_label = tk.Label(pos_frame, text="Put Price: -", font=("Helvetica", 12), anchor="w")
    put_label.grid(row=2, column=0, sticky='w', padx=5, pady=(5, 10))

    #tk.Button(pos_frame, text="Add/Update Put Position").grid(row=2, column=1, sticky='w', padx=10, pady=(5, 10))
    # tk.Button(pos_frame, text="Update Put Positions in Portolio Tab", 
    #       command=lambda: update_positions(get_current_option_data("put")))\
    #       .grid(row=2, column=1, pady=10)

    pos_frame.columnconfigure(1, weight=1)
    calculate()


    return pricer_tab
