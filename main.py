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


def setup_from_combobox(master, variable):
    from_combobox = ttk.Combobox(master, textvariable=variable, values=list(converter.currencies.keys()), width=10)
    from_combobox.place(relx=0.5, rely=0.15, anchor='center')
    from_combobox.bind('<KeyRelease>', lambda event: key_release_handler(event, from_combobox, variable))
    return from_combobox

def setup_to_combobox(master, variable):
    to_combobox = ttk.Combobox(master, textvariable=variable, values=list(converter.currencies.keys()), width=10)
    to_combobox.place(relx=0.5, rely=0.25, anchor='center')
    to_combobox.bind('<KeyRelease>', lambda event: key_release_handler(event, to_combobox, variable))
    return to_combobox

def key_release_handler(event, combobox, variable):
    content = combobox.get().upper()
    filtered_content = ''.join(filter(str.isalpha, content))
    valid_content = filtered_content[:3]
    variable.set(valid_content)
    update_combobox_options(combobox, variable)

def update_combobox_options(combobox, variable):
    typed_value = combobox.get().upper()
    all_currencies = list(converter.currencies.keys())

    filtered_options = [currency for currency in all_currencies if typed_value in currency]

    if typed_value:
        combobox['values'] = filtered_options

        matches = difflib.get_close_matches(typed_value, filtered_options, n=1, cutoff=0.6)
        if matches:
            closest_match = matches[0]
            if typed_value != closest_match and len(typed_value) >= len(closest_match) - 1:
                variable.set(closest_match)
    else:
        combobox['values'] = all_currencies

def conversion():
    source_currency = source_currency_var.get().upper()
    target_currency = target_currency_var.get().upper()
    amount = amount_entry.get()

    if source_currency not in converter.currencies or target_currency not in converter.currencies:
        error_label.config(text="Invalid currency code", foreground="red")
        return

    if not amount.replace('.', '', 1).isdigit():
        error_label.config(text="Please enter a valid number", foreground="red")
        return

    error_label.config(text="")

    amount = float(amount)
    response = requests.get(f'https://www.x-rates.com/calculator/?from={source_currency}&to={target_currency}&amount=1')
    soup = bs(response.text, 'html.parser')
    rate = float(soup.find('span', class_='ccOutputTrail').previous_sibling.replace(',', ''))
    result = amount * rate

    save_data(source_currency, target_currency, amount, result)
    
    result_text = f"{amount:.2f} {source_currency} is {result:.5f} {target_currency}"
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

def enforce_decimal_limit(event):
    content = amount_entry.get()
    if '.' in content:
        parts = content.split('.')
        if len(parts) > 1 and len(parts[1]) > 2:
            new_content = parts[0] + '.' + parts[1][:2]
            amount_entry.delete(0, tk.END)
            amount_entry.insert(0, new_content)

converter = CurrencyConverter('currencies.json')

conversion_app = tk.Tk()
conversion_app.title('Currency Converter')
conversion_app.geometry('350x300')
conversion_app.configure(bg='black')
conversion_app.eval('tk::PlaceWindow . center')
conversion_app.resizable(False, False)

style = ttk.Style()
style.theme_use('default')
style.configure('TLabel', background='black', foreground='white')
style.configure('TButton', background='white', foreground='black')
style.configure('TCheckbutton', background='black', foreground='white')
style.configure('TEntry', justify='center', background='white', foreground='black')
style.configure('TCombobox', fieldbackground='white', background='white', foreground='black')

source_currency_var = tk.StringVar(conversion_app)
target_currency_var = tk.StringVar(conversion_app)

ttk.Label(conversion_app, text='From:', font='Arial 10 bold').place(relx=0.3, rely=0.15, anchor='center')
ttk.Label(conversion_app, text='To:', font='Arial 10 bold').place(relx=0.3, rely=0.25, anchor='center')
ttk.Label(conversion_app, text='Amount:', font='Arial 10 bold').place(relx=0.13, rely=0.4, anchor='center')

amount_entry = ttk.Entry(conversion_app, font='Arial 10', justify='center')
amount_entry.place(relx=0.5, rely=0.4, anchor='center')
amount_entry.bind('<KeyRelease>', enforce_decimal_limit)

button_convert = ttk.Button(conversion_app, text='Convert', command=conversion)
button_convert.place(relx=0.5, rely=0.5, anchor='center')

button_clear = ttk.Button(conversion_app, text='Clear', command=clear)
button_clear.place(relx=0.5, rely=0.6, anchor='center')

result_label = ttk.Label(conversion_app, font='Arial 10 bold', foreground='green')
result_label.place(relx=0.5, rely=0.7, anchor='center')

error_label = ttk.Label(conversion_app, font='Arial 10', foreground='red')
error_label.place(relx=0.5, rely=0.9, anchor='center')

setup_from_combobox(conversion_app, source_currency_var)
setup_to_combobox(conversion_app, target_currency_var)

conversion_app.mainloop()
