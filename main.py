from gui.pricing_gui import launch_gui
from gui.portfolio_gui import launch_portfolio_tab

import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Options Toolkit")
    root.geometry("1500x1000")  # Optional: make it a bit wider

    # Create the tab control
    notebook = ttk.Notebook(root)  
    notebook.pack(expand=True, fill='both')

    launch_gui(notebook)

    # Create blank tabs
    #pricer_tab = ttk.Frame(notebook)
    positions_tab = ttk.Frame(notebook)
    notebook.add(positions_tab, text="Positions")

    launch_portfolio_tab(positions_tab)


    chart_tab = ttk.Frame(notebook)
    notebook.add(chart_tab, text="Time Chart")

    root.mainloop()

    

   


if __name__ == "__main__":
    main()