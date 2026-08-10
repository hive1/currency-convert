'''
In order to build a currency converter, we need to create a class that can handle different currencies and their conversion rates. 
The class should be able to store the currency name, symbol, and conversion rate to a base currency (e.g., USD). 
It should also provide methods to convert amounts between different currencies.

No AI challenge

To begin:
- Class with attributes for currency name, symbol, and conversion rate.

I guess in theory, conversion rate can technically be the percentage of the base currency, but for simplicity, we will use a direct conversion rate (e.g., 1 USD = 0.85 EUR).
'''
import requests
from decimal import Decimal

e_url = 'https://v6.exchangerate-api.com/v6/bc1b3aa3b38cbc50bb5f1457/latest/USD'

class Currency:
    '''Base currency is USD'''

    def __init__(self, name, symbol, conversion_rate):
        self.name = name
        self.symbol = symbol,
        self.conversion_rate = conversion_rate

    def convert(self, target):
        # So at this point I would request the json of conversion rates based on 
        pass

# Return the abbreviated input
def find(input):

    from csv import DictReader

    with open("currency_names.csv") as newfile:
        reader = DictReader("currency_names.csv")
        for row in reader:
            print(row)
    comparison = DictReader("currency_names.csv", dialect='excel')

    for x in comparison:
        print(x)

def __main__():
    response = requests.get(e_url)
    exchange_json = response.json()

    # Creating a dictionary from the received json
    
    exchanges = {}
    string_exchange = str(exchange_json['conversion_rates'])
    list_se = string_exchange.split(',')
    for value in list_se:
        ab, ex = value.split(":")

        ab = ab.replace("'","")
        print(ab)

        # Make sure that no {} get caught in the filter process
        ex = Decimal(ex.replace("}",""))
        print(ex)

        exchanges.update({ab[1:]: ex})

    # print(exchanges)
    print(find(ab))



__main__()
