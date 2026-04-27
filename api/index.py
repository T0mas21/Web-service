from flask import Flask, request, jsonify
import requests
from simpleeval import simple_eval

app = Flask(__name__)

AIRPORT_INFO_URL = "https://www.airport-data.com/api/ap_info.json"

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

STOCK_API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"


def get_airport_temperature(iata):
    try:
        air_res = requests.get(f"{AIRPORT_INFO_URL}?iata={iata}").json()
        lat, lon = air_res['latitude'], air_res['longitude']
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }
        w_res = requests.get(WEATHER_API_URL, params=params).json()
        return float(w_res['current_weather']['temperature'])
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
        return "Error in expression"


@app.route('/')
def handle_query():
    q_eval = request.args.get('queryEval')
    q_stock = request.args.get('queryStockPrice')
    q_temp = request.args.get('queryAirportTemp')

    if q_eval is not None:
        result = evaluate_expression(q_eval)
    elif q_stock is not None:
        result = get_stock_price(q_stock)
    elif q_temp is not None:
        result = get_airport_temperature(q_temp)
    else:
        result = None

    return jsonify(result)

if __name__ == "__main__":
    app.run()

    