from flask import Flask, request, jsonify
import requests
from simpleeval import simple_eval

app = Flask(__name__)


STOCK_API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"


def get_airport_temperature(iata):
    try:
        headers = {'User-Agent': 'curl/7.64.1'}
        url = f"https://wttr.in/{iata}?format=j1"
        res = requests.get(url, headers=headers).json()
        
        temp = res['current_condition'][0]['temp_C']
        return float(temp)
    except Exception:
        return None

def get_stock_price(symbol):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(f"{STOCK_API_URL}{symbol}", headers=headers).json()
        return float(res['chart']['result'][0]['meta']['regularMarketPrice'])
    except Exception:
        return None

def evaluate_expression(expression):
    try:
        return float(simple_eval(expression))
    except Exception:
        return None


@app.route('/')
def handle_query():
    q_eval = request.args.get('queryEval')
    q_stock = request.args.get('queryStockPrice')
    q_temp = request.args.get('queryAirportTemp')

    result = None

    if q_eval is not None:
        result = evaluate_expression(q_eval)
    elif q_stock is not None:
        result = get_stock_price(q_stock)
    elif q_temp is not None:
        result = get_airport_temperature(q_temp)

    return jsonify(result)

if __name__ == "__main__":
    app.run()