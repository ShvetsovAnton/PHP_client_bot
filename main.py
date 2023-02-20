import os

import requests
from dotenv import load_dotenv


load_dotenv()
db_username = os.getenv('DP_USER_NAME')
db_password = os.getenv('DP_PASSWORD')


def verification_access(message):
    tg_username = message['from']['username']
    url = 'http://bombard.tech/client/'
    params = {'username': tg_username}
    response = requests.get(
        url,
        params=params,
        auth=(db_username, db_password)
    )
    response.raise_for_status()
    if response.json():
        return (response.json()['username'],
                response.json()['id'],
                message['from']['id'])
    return


def make_new_order(new_order, order_description):
    tg_user_id = order_description['tg_user_id']
    dp_user_id = order_description['dp_user_id']
    order_text = new_order['text']
    url = 'http://bombard.tech/orders/'
    params = {
        "client_tg_id": tg_user_id,
        "client": f"http://bombard.tech/clients/{dp_user_id}/",
        "text": order_text
    }
    response = requests.post(url, data=params, auth=(db_username, db_password))
    response.raise_for_status()
    return response.json()['id']


def send_secretkey(order, order_description):

    order_id = order_description['order_id']
    url = f'http://bombard.tech/orders/{order_id}/'
    params = {'credentials': 'bla'}
    response = requests.patch(
        url,
        data=params,
        auth=(db_username, db_password)
    )
    response.raise_for_status()

