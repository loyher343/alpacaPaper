import json, requests
from chalicelib.config import *
from chalicelib.mail_man import *
from chalice import Chalice



app = Chalice(app_name='tradingwiew-webhook-alerts')


BASE_URL = "https://paper-api.alpaca.markets"
CLOCK_URL = "{}/v2/clock".format(BASE_URL)
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL ="{}/v2/orders".format(BASE_URL)
POSITIONS_URL="{}/v2/positions/SPXL".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

@app.route('/')
def index():
    bot_message(EMAIL, PASSWORD, RECIPIENT)
    return {'hello': 'world'}


@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    #setup

    get_market_hours = requests.get(CLOCK_URL, headers=HEADERS)
    market_hours = get_market_hours.json()
    open_close = market_hours['is_open']

    #gets account info
    get_account = requests.get(ACCOUNT_URL, headers=HEADERS)
    account_response = json.loads(get_account.content)

    acc_info = {
        "BP" : account_response['buying_power'],
        "regt_BP": account_response['regt_buying_power'],
        "day_count" : account_response['daytrade_count'],
    }


    #gets postion data
    position_request = requests.get(POSITIONS_URL, headers=HEADERS)
    position_response = json.loads(position_request.content)
    print(position_response)
    position = {
        "message":  ' ',
        "qty": ' '

    }
    #webhook data catcher
    request = app.current_request
    webhook_message = request.json_body
    data = {
        "side": webhook_message['buy/sell'],                    # buy or sell
        "symbol": webhook_message['ticker'],
        "qty": 1,                           
        "type": "market",                                        # market, limit, stop, stop_limit, or trailing_stop
        "limit_price": webhook_message['close'],                # required if type is limit or stop_limit
        "time_in_force": "gtc",                                 # day, gtc, opg, cls, ioc, fok.
    }


    
    #stops if daytrade exceeded
    if acc_info['day_count'] > 3:
        return 
    elif float(acc_info['regt_BP']) < float(data['limit_price']):
        return 'not enough BP'


    #if there is a message do nothing else update qty of asset
    if 'message' in position_response:
        print(position_response['message'])
    else:
        position = {
            "qty": position_response['qty']
        }
    

    #email message setup
    mail_message = 'MERP'
    if data['side'] == 'buy':
        buy_shares = float(acc_info["regt_BP"])//float(data['limit_price'])
        print(buy_shares)
        data['qty'] = buy_shares
        mail_message = 'Buying '+str(buy_shares)+' shares'
    elif data['side'] == 'sell':
        data['qty'] = position['qty']
        mail_message = 'Selling '+str(data['qty'])+' shares'
    email_text =mail_message+' Tendies be lookin like '+str(account_response['equity'])


    #change to limit if closed
    if open_close != True:
        data['type'] = 'limit'


    #order request
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    response = json.loads(r.content)



    print(response)
    send(EMAIL, PASSWORD, RECIPIENT, email_text)
    return {
        'message': 'I bought the stock :)',
    }



