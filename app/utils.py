import requests

def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        response = requests.get(url)
        data = response.json()

        return data['quoteResponse']['result'][0]['regularMarketPrice']
    except:
        return None