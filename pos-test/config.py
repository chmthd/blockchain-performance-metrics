from web3 import Web3

MY_ADDRESS = '123463a4b065722e99115d6c222f267d9cabb524'
PRIVATE_KEY = '0x72457db75d08355a4bec8c85a5af7ecd1d005f01fabbb1862d2abf98535a98e5'
RECIPIENT_ADDRESS = '0x69abB3Ca799A6431a7ff8df7C01aC16073e1ED89'
NUM_BLOCKS = 200

def connect():
    node_url = 'http://127.0.0.1:8000'
    w3 = Web3(Web3.HTTPProvider(node_url))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to the Ethereum node at " + node_url)
    print("Successfully connected to Ethereum node")
    return w3
