import hashlib
import hmac
import json
import uuid
import requests


ID_PROJECT = 'You ID PROJECT'
SECRET_KEY = 'You secret key'



def sort_dict(_data: dict):
    return dict(sorted(_data.items(), key=lambda x: x[0]))


def make_sign(_data):
    data = sort_dict(_data)
    sign = hmac.new(bytes(SECRET_KEY, 'UTF-8'), json.dumps(data).encode(), hashlib.sha256).hexdigest()
    return sign


def get_balance():
    result = {'success': False, 'balance': 0.00}
    data = {
        'shopId': ID_PROJECT,
    }
    response = requests.post(f'https://api.lava.ru/business/shop/get-balance', json=data,
                             headers={'Signature': make_sign(data), 'Accept': 'application/json',
                                      'Content-Type': 'application/json'}).json()
    if response['status'] == 200:
        result['success'] = True
        result['balance'] = response['data']['balance']
    return result


def get_pay_method():
    result = {'success': False, 'pay_method': []}
    data = {
        'shopId': ID_PROJECT,
        'signature': SECRET_KEY
    }
    response = requests.post(f'https://api.lava.ru/business/invoice/get-available-tariffs', json=data,
                             headers={'Signature': make_sign(data), 'Accept': 'application/json',
                                      'Content-Type': 'application/json'}).json()
    if response['status'] == 200:
        result['success'] = True
        result['pay_method'] = response['data']
    return result


def create_order(amount: float = 0.00, order_id: str = 'Идентификатор платежа', purpose: str = 'Назначение платежа'):
    result = {'success': False, 'invoice_id': None}
    data = {
        "comment": purpose,
        "customFields": "None",
        "expire": 300,
        "failUrl": "https://steamup.market/api/lava/error",
        "hookUrl ": "https://steamup.market/api/lava/hook",
        "includeService": ["card", "sbp", "qiwi"],
        "orderId": order_id,
        'shopId': ID_PROJECT,
        "successUrl": "https://steamup.market/api/lava/success",
        'sum': amount,
    }
    response = requests.post(f'https://api.lava.ru/business/invoice/create', json=data,
                             headers={'Signature': make_sign(data), 'Accept': 'application/json',
                                      'Content-Type': 'application/json'}).json()
    if response['status'] == 200:
        result['success'] = True
        result['invoice_id'] = response['data']['id']
    return result


def status_order(invoice_id: uuid = None):
    result = {'success': False, 'status': None}
    data = {
        "invoiceId": invoice_id,
        "shopId": ID_PROJECT,
    }
    response = requests.post(f'https://api.lava.ru/business/invoice/status', json=data,
                             headers={'Signature': make_sign(data), 'Accept': 'application/json',
                                      'Content-Type': 'application/json'}).json()
    if response['status'] == 200:
        result['success'] = True
        result['status'] = response['data']['status']
    return result


if __name__ == '__main__':
    # print(get_balanse())
    # print(get_pay_method())
    # _bal = create_order(10, 2)
    print(create_order(10.5, '12346'))
    # _ = status_order('3113de6d-4a6f-4769-bc39-12c0f60aa51d')
    pass


