import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup as bs
import json

class CurrencyConverter:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            self.currencies = json.load(file)

def setup_combobox(master, variable, row, column):
    combobox = ttk.Combobox(master, textvariable=variable, values=list(converter.currencies.keys()), width=3)
    combobox.grid(row=row, column=column, sticky='ew', padx=5, pady=5)
    combobox.bind('<KeyRelease>', lambda event: [combobox.set(combobox.get().upper()), update_combobox_options(combobox)])
    return combobox

def update_combobox_options(combobox):
    value = combobox.get()
    filtered_options = [currency for currency in converter.currencies if value in currency]
    combobox['values'] = filtered_options
    if value not in filtered_options:
        combobox.set(value)

def conversion():
    source_currency = source_currency_var.get()
    target_currency = target_currency_var.get()
    amount = amount_entry.get()

    if not amount.replace('.', '', 1).isdigit():
        error_label.config(text="Please enter a valid number", fg="white")
        return

    amount = float(amount)
    response = requests.get(f'https://www.x-rates.com/calculator/?from={source_currency}&to={target_currency}&amount={amount}')
    soup = bs(response.text, 'html.parser')
    rate = float(soup.find('span', class_='ccOutputTrail').previous_sibling.replace(',', ''))
    result = amount * rate
    result = result / 10

    save_data(source_currency, target_currency, amount, result, rounded_var.get())

    if rounded_var.get() == 1:
        result = round(result, 2)
    
    result_label.config(text=f"{amount} {source_currency} is {result} {target_currency}")

def clear():
    source_currency_var.set('')
    target_currency_var.set('')
    amount_entry.delete(0, tk.END)
    result_label.config(text='')
    error_label.config(text='')

def save_data(source, target, amount, result, rounded):
    data = {
        "source_currency": source,
        "target_currency": target,
        "amount": amount,
        "result": result,
        "rounded": bool(rounded)
    }
    with open("calculation_entry_data.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

converter = CurrencyConverter('currencies.json')

conversion_app = tk.Tk()
conversion_app.title('Currency Converter')
conversion_app.geometry('700x500')
conversion_app.configure(bg='black')

style = ttk.Style()
style.theme_use('default')
style.configure('TLabel', background='black', foreground='white')
style.configure('TButton', background='white', foreground='black')
style.configure('TCheckbutton', background='black', foreground='white')
style.configure('TEntry', background='white', foreground='black')
style.configure('TCombobox', fieldbackground='white', background='white', foreground='black')

source_currency_var = tk.StringVar(conversion_app)
target_currency_var = tk.StringVar(conversion_app)
rounded_var = tk.IntVar(conversion_app)

ttk.Label(conversion_app, text='From:', font='Calibri 12').grid(row=0, column=4, pady=10)
ttk.Label(conversion_app, text='To:', font='Calibri 12').grid(row=1, column=4, pady=10)
ttk.Label(conversion_app, text='Amount:', font='Calibri 12').grid(row=2, column=4, pady=10)

amount_entry = ttk.Entry(conversion_app, font='Calibri 12')
amount_entry.grid(row=2, column=5, pady=5, sticky='ew')

result_label = ttk.Label(conversion_app, font='Calibri 12 bold', foreground='green')
result_label.grid(row=8, column=5, sticky='w')

error_label = ttk.Label(conversion_app, font='Calibri 10', foreground='red')
error_label.grid(row=9, column=4, columnspan=2)

check_rounded = ttk.Checkbutton(conversion_app, text="Round to 2 decimal places", variable=rounded_var)
check_rounded.grid(row=3, column=5, pady=5, sticky='w')

button_convert = ttk.Button(conversion_app, text='Convert', command=conversion)
button_convert.grid(row=4, column=5, pady=5, sticky='ew')

button_clear = ttk.Button(conversion_app, text='Clear', command=clear)
button_clear.grid(row=5, column=5, pady=5, sticky='ew')

setup_combobox(conversion_app, source_currency_var, 0, 1)
setup_combobox(conversion_app, target_currency_var, 1, 1)

conversion_app.mainloop()
