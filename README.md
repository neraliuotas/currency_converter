# Currency Converter

This Currency Converter is a simple desktop application built with Python and Tkinter. It allows users to convert amounts between various currencies using up-to-date exchange rates fetched from an external API.

## Features

- **Simple and Intuitive UI**: A user-friendly interface that allows quick and easy currency conversions.
- **Real-time Conversion Rates**: Fetches the latest conversion rates from a reliable financial data API.
- **Support for Multiple Currencies**: Includes a wide range of currencies from around the world.
- **Input Validation**: Ensures that the user inputs are valid currency codes and amounts.
- **Error Handling**: Provides feedback to the user if there's an error with their input or a problem with the data source.

## Installation

To run the Currency Converter on your local machine, you need to have Python installed. Clone the repository to your local machine:

```bash
git clone https://github.com/neraliuotas/currency-converter.git
cd currency-converter
```

Before running the application, install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

To start the application, run:

```
python currency_converter.py
```

Once the application is running:

1. Select the currency code from the 'From' dropdown that you want to convert from.
2. Select the currency code from the 'To' dropdown that you want to convert to.
3. Enter the amount you want to convert.
4. Click 'Convert' to see the converted amount.
5. If needed, click 'Clear' to reset the form and start a new conversion.

## Contributing

Contributions to the Currency Converter project are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/fooBar`).
3. Commit your changes (`git commit -am 'Add some fooBar'`).
4. Push to the branch (`git push origin feature/fooBar`).
5. Create a new Pull Request.

## Licence

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

* Currency data provided by [X-Rates](https://www.x-rates.com)
* Programming teacher [infohata](https://github.com/infohata)
