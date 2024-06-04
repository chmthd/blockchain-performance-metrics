import csv
import time
import concurrent.futures
import matplotlib.pyplot as plt

from web3 import Web3, Account
from config import connect, PRIVATE_KEY, RECIPIENT_ADDRESS

w3 = connect()
acct = Account.from_key(PRIVATE_KEY)


def send_transaction(nonce):
    tx = {
        'to': RECIPIENT_ADDRESS,
        'value': w3.to_wei(1, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.to_wei('500', 'gwei'),
        'nonce': nonce,
        'chainId': 32382
    }
    signed_tx = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_sent_timestamp = time.time()

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    tx_confirmed_timestamp = time.time()
    return tx_hash.hex(), tx_sent_timestamp, tx_confirmed_timestamp


def collect_data(num_transactions):
    start_nonce = w3.eth.get_transaction_count(acct.address)
    transactions_data = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_transaction, start_nonce + i) for i in range(num_transactions)]
        for future in concurrent.futures.as_completed(futures):
            transactions_data.append(future.result())
    return transactions_data


def write_to_csv(data, filename='transaction_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction Hash', 'Timestamp Sent', 'Timestamp Confirmed'])
        for row in data:
            writer.writerow(row)


def main():
    offered_loads = [5, 50, 100, 200, 500, 1000]
    throughputs = []

    for load in offered_loads:
        transactions_data = collect_data(load)
        total_time = max([tx[2] for tx in transactions_data]) - min([tx[1] for tx in transactions_data])
        throughput = load / total_time
        throughputs.append(throughput)
        print(f"Offered Load: {load}, Throughput: {throughput} transactions per second")

    plt.figure(figsize=(12, 7))
    plt.plot(offered_loads, throughputs, 'o-', color='#6e57d2', label='Throughput vs Offered Load')
    plt.title('Impact of Load Variation on Transaction Throughput in a 5-Node PoS Network')
    plt.xlabel('Number of Transactions')
    plt.ylabel('Throughput (TPS)')
    plt.xticks(offered_loads)
    plt.legend()
    plt.grid(True)
    plt.savefig('throughput.png')
    plt.show()


if __name__ == "__main__":
    main()
