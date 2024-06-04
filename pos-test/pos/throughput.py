from connection import connect
import time
import matplotlib.pyplot as plt

# Connect to Ethereum node
w3 = connect()
my_address = w3.to_checksum_address('123463a4b065722e99115d6c222f267d9cabb524')
private_key = '0x72457db75d08355a4bec8c85a5af7ecd1d005f01fabbb1862d2abf98535a98e5'

def send_transaction(nonce):
    transaction = {
        'to': w3.to_checksum_address('0xfe8664457176d0f87eaabd103aba410855f81010'),
        'value': w3.to_wei(0.01, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('40', 'gwei'),
        'nonce': nonce,
        'chainId': 32382
    }
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return txn_hash

def monitor_throughput(duration_seconds, batch_size):
    start_time = time.time()
    end_time = start_time + duration_seconds
    nonce = w3.eth.get_transaction_count(my_address, 'pending')
    transactions = []
    while time.time() < end_time:
        for _ in range(batch_size):
            try:
                txn_hash = send_transaction(nonce)
                transactions.append(txn_hash)
                nonce += 1  # Increment nonce only on sending
            except ValueError as e:
                if 'nonce too low' in str(e):
                    nonce = w3.eth.get_transaction_count(my_address, 'pending')  # Refetch nonce
                else:
                    print(f"Error: {e}")
        time.sleep(1)  # Wait a second before sending next batch

    confirmed_transactions = 0
    for txn_hash in transactions:
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        if receipt.status == 1:
            confirmed_transactions += 1

    return confirmed_transactions / duration_seconds

def plot_throughput(tps_values):
    plt.figure(figsize=(10, 5))
    plt.plot(tps_values, marker='o')
    plt.title('Transaction Throughput Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Transactions Per Second (TPS)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    tps = monitor_throughput(60, 1)  # Monitor for 60 seconds, attempting to send 10 transactions per second
    print(f"Average TPS: {tps}")
    plot_throughput([tps])
