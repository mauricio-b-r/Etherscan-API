import requests
from django.conf import settings


params_latest_block_number = {"module": "proxy", "action": "eth_blockNumber"}
params_block_by_number = {
    "module": "proxy",
    "action": "eth_getBlockByNumber",
    "boolean": False,
    "tag": "",
}
params_transactions_by_address = {
    "module": "account",
    "action": "txlist",
    "address": "",
    "startblock": 0,
    "endblock": 99999999,
    "page": 1,
    "offset": 10,
    "sort": "asc",
}
params_transaction_by_transaction_hash = {
    "module": "proxy",
    "action": "eth_getTransactionByHash",
    "txhash": "",
}


def get_request(params):
    api_url = settings.ETHERSCAN_API_URL
    api_key = settings.ETHERSCAN_API_KEY
    params["apiKey"] = api_key

    return requests.get(api_url, params)


def get_latest_block_number_request():
    return get_request(params_latest_block_number)


def get_block_by_number_request(blockno):
    params = params_block_by_number
    params["tag"] = blockno
    return get_request(params)


def get_transactions_by_address_request(address="", page=1):
    params = params_transactions_by_address
    params["address"] = address
    params["page"] = page
    return get_request(params)


def get_transaction_by_transaction_hash_request(tx_hash):
    params = params_transaction_by_transaction_hash
    params["txhash"] = tx_hash
    return get_request(params)
