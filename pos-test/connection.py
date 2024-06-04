from web3 import Web3

def connect():
    node_url = 'http://127.0.0.1:8501'
    w3 = Web3(Web3.HTTPProvider(node_url))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to the Ethereum node at " + node_url)
    print("Successfully connected to Ethereum node")
    return w3


