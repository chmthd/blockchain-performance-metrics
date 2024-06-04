from connection import connect
from config import PRIVATE_KEY

# setup
w3 = connect()

# account setup
account_from = {
    'private_key':PRIVATE_KEY,  
    'address': w3.to_checksum_address('0x123463a4b065722e99115d6c222f267d9cabb524'),  
}
account_to = w3.to_checksum_address('0x5C147AFcC6d66A8d110CFF2278CCAB66A9dbFb05')  

# send tx
def send_transaction(w3, account_from, to_address, amount):
    nonce = w3.eth.get_transaction_count(account_from['address'])
    txn_dict = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.to_wei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'chainId': 32382  
    }

    signed_txn = w3.eth.account.sign_transaction(txn_dict, account_from['private_key'])
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(f"Transaction successful with hash: {txn_hash.hex()}")

send_transaction(w3, account_from, account_to, 0.1)

