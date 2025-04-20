from gui.pricing_gui import launch_gui

import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Options Toolkit")
    root.geometry("1200x800")  # Optional: make it a bit wider

    # Create the tab control
    notebook = ttk.Notebook(root)  
    notebook.pack(expand=True, fill='both')

    launch_gui(notebook)

    # Create blank tabs
    pricer_tab = ttk.Frame(notebook)
    heatmap_tab = ttk.Frame(notebook)
    chart_tab = ttk.Frame(notebook)

    # Add tabs to notebook
    notebook.add(heatmap_tab, text="Heatmap")
    notebook.add(chart_tab, text="Time Chart")
   

    # Add placeholder content (optional)
    ttk.Label(pricer_tab, text="Pricer UI goes here").grid(pady=20)
    #ttk.Label(heatmap_tab, text="Heatmap will be displayed here").pack(pady=20)
    #ttk.Label(chart_tab, text="Chart will be displayed here").pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()