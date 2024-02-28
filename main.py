import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup as bs
import json
import difflib

class CurrencyConverter:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            self.currencies = json.load(file)


def setup_combobox(master, variable, row, column):
    combobox = ttk.Combobox(master, textvariable=variable, values=list(converter.currencies.keys()), width=3)
    combobox.grid(row=row, column=column, sticky='n', padx=5, pady=5)
    combobox.bind('<KeyRelease>', lambda event: [combobox.set(combobox.get().upper()), update_combobox_options(combobox, variable)])
    return combobox

def update_combobox_options(combobox, variable):
    typed_value = combobox.get().upper()
    all_currencies = list(converter.currencies.keys())
    
    filtered_options = [currency for currency in all_currencies if typed_value in currency]
    
    if typed_value:
        matches = difflib.get_close_matches(typed_value, filtered_options, n=1, cutoff=0.6)
        if matches:
            closest_match = matches[0]
            if typed_value != closest_match:
                combobox['values'] = [closest_match] + [currency for currency in filtered_options if currency != closest_match]
                variable.set(closest_match)
            else:
                combobox['values'] = filtered_options
        else:
            combobox['values'] = filtered_options
    else:
        combobox['values'] = all_currencies

def conversion():
    source_currency = source_currency_var.get()
    target_currency = target_currency_var.get()
    amount = amount_entry.get()

    if not amount.replace('.', '', 1).isdigit():
        error_label.config(text="Please enter a valid number", foreground="white")
        return

    amount = float(amount)
    response = requests.get(f'https://www.x-rates.com/calculator/?from={source_currency}&to={target_currency}&amount={amount}')
    soup = bs(response.text, 'html.parser')
    rate = float(soup.find('span', class_='ccOutputTrail').previous_sibling.replace(',', ''))
    result = (amount * rate) / 100

    save_data(source_currency, target_currency, amount, result)
    
    result_text = f"{amount:.2f} {source_currency} is {result:.4f} {target_currency}"
    result_label.config(text=result_text[:5] + result_text[5:])

def clear():
    source_currency_var.set('')
    target_currency_var.set('')
    amount_entry.delete(0, tk.END)
    result_label.config(text='')
    error_label.config(text='')

def save_data(source, target, amount, result):
    data = {
        "source_currency": source,
        "target_currency": target,
        "amount": amount,
        "result": result,
    }
    with open("calculation_entry_data.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

converter = CurrencyConverter('currencies.json')

conversion_app = tk.Tk()
conversion_app.title('Currency Converter')
conversion_app.geometry('350x300')
conversion_app.configure(bg='black')
conversion_app.eval('tk::PlaceWindow . center')

style = ttk.Style()
style.theme_use('default')
style.configure('TLabel', background='black', foreground='white')
style.configure('TButton', background='white', foreground='black')
style.configure('TCheckbutton', background='black', foreground='white')
style.configure('TEntry', justify='center', background='white', foreground='black')
style.configure('TCombobox', fieldbackground='white', background='white', foreground='black')

source_currency_var = tk.StringVar(conversion_app)
target_currency_var = tk.StringVar(conversion_app)

ttk.Label(conversion_app, text='From:', font='Calibri 12').grid(row=0, column=1, pady=(15, 0))
ttk.Label(conversion_app, text='To:', font='Calibri 12').grid(row=1, column=1, pady=(15, 0))
ttk.Label(conversion_app, text='Amount:', font='Calibri 12').grid(row=2, column=1, pady=(12, 0))

widget_width = 200
widget_height = 25

x_position = (350 - widget_width) / 2
y_positions = {
    'amount_entry': 85,
    'button_convert': 115,
    'button_clear': 145,
    'error_label': 205,
}

amount_entry = ttk.Entry(conversion_app, font='Calibri 12')
amount_entry.place(x=x_position-1, y=y_positions['amount_entry'], width=widget_width, height=widget_height)

result_label = ttk.Label(conversion_app, font='Calibri 12 bold', foreground='green')
result_label.place(relx=0.5, rely=0.61, anchor='center')

error_label = ttk.Label(conversion_app, font='Calibri 10', foreground='red')
error_label.place(x=x_position, y=y_positions['error_label'], width=widget_width, height=widget_height)

button_convert = ttk.Button(conversion_app, text='Convert', command=conversion)
button_convert.place(x=x_position, y=y_positions['button_convert'], width=widget_width, height=widget_height)

button_clear = ttk.Button(conversion_app, text='Clear', command=clear)
button_clear.place(x=x_position, y=y_positions['button_clear'], width=widget_width, height=widget_height)

setup_combobox(conversion_app, source_currency_var, 0, 1)
setup_combobox(conversion_app, target_currency_var, 1, 1)

conversion_app.mainloop()
