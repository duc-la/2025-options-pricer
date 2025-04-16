from tkinter import ttk

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

notebook.add(tab1, text='Options Pricer')
notebook.add(tab2, text='Heatmap')
notebook.add(tab3, text='Time Chart')