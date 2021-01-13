import json, requests
from config import *
from chalice import Chalice


app = Chalice(app_name='tradingwiew-webhook-alerts')


BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL ="{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

# @app.route('/')
# def index():
#     return {'yo'}

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    request = app.current_request
    webhook_message = request.json_body
    data = {
        "side": webhook_message['buy/sell'],
        "symbol": webhook_message['ticker'],
        "qty": 1,
        "side": "buy",                                          # buy or sell
        "type": "limit",                                        # market, limit, stop, stop_limit, or trailing_stop
        "limit_price": webhook_message['close'],                # required if type is limit or stop_limit
        "time_in_force": "gtc",                                 # day, gtc, opg, cls, ioc, fok.
        "order_class": "bracket",                               # simple, bracket, oco or oto.
        "take_profit": {
            "limit_price": webhook_message['close'] * 1.05
        },
        "stop_loss": {
            "stop_price": webhook_message['close'] * 0.98,
        }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    response = json.loads(r.content)

    print(response)
    print('///////',response['id'],'////////')
   
    return {
        'message': 'I bought the stock',
        'webhook_message': webhook_message
    }

