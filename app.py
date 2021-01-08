import json, requests
from config import *
from chalice import Chalice


app = Chalice(app_name='tradingwiew-webhook-alerts')

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL ="{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    request = app.current_request
    webhook_message = request.json_body
    data = {
        "buy/sell": webhook_message['buy/sell'],
        "symbol": webhook_message['ticker'],
        "qty": 1,
        "side": "buy",
        "type": "limit",
        "limit_price": webhook_message['close'],
        "time_in_force": "gtc",
        "order_class": "bracket",
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

#28:00


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#


# {
#     "open": {{open}},
#     "high": {{high}},
#     "low": {{low}},
#     "close": {{close}},
#     "exchange": "{{exchange}}",
#     "ticker": "{{ticker}}",
#     "volume": {{volume}},
#     "time": "{{time}}",
#     "timenow": "{{timenow}}"
# }