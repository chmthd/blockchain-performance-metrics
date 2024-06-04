import csv
import time
import concurrent.futures
import matplotlib.pyplot as plt
from web3 import Web3, Account
from config import connect, PRIVATE_KEY, RECIPIENT_ADDRESS

# Initialize connection and account
w3 = connect()
acct = Account.from_key(PRIVATE_KEY)

def send_transaction(nonce, gas_price):
    tx = {
        'to': RECIPIENT_ADDRESS,
        'value': w3.to_wei(1, 'ether'),
        'gas': 21000,  # Typical gas limit for a simple transfer
        'gasPrice': w3.to_wei(gas_price, 'gwei'),
        'nonce': nonce,
        'chainId': 32382
    }
    signed_tx = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_sent_timestamp = time.time()

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    tx_confirmed_timestamp = time.time()
    return tx_hash.hex(), tx_sent_timestamp, tx_confirmed_timestamp

def collect_data(num_transactions, gas_price):
    start_nonce = w3.eth.get_transaction_count(acct.address, 'pending')
    transactions_data = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_transaction, start_nonce + i, gas_price) for i in range(num_transactions)]
        for future in concurrent.futures.as_completed(futures):
            transactions_data.append(future.result())
    
    return transactions_data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction Hash', 'Timestamp Sent', 'Timestamp Confirmed'])
        for row in data:
            writer.writerow(row)

def main():
    gas_prices = [50, 100, 500, 1000, 5000]  # in gwei
    throughput_data = []

    for gas_price in gas_prices:
        transactions_data = collect_data(100, gas_price)
        total_time = max(tx[2] for tx in transactions_data) - min(tx[1] for tx in transactions_data)
        throughput = 100 / total_time
        throughput_data.append((gas_price, throughput))
        print(f"Gas Price: {gas_price} gwei, Throughput: {throughput:.2f} transactions per second")

        write_to_csv(transactions_data, f'transaction_data_{gas_price}gwei.csv')

    plt.figure(figsize=(10, 5))
    plt.plot([gp[0] for gp in throughput_data], [tp[1] for tp in throughput_data], marker='o', linestyle='-', color='#6e57d2')
    plt.title('Impact of Gas Price on Transaction Throughput')
    plt.xlabel('Gas Price (gwei)')
    plt.ylabel('Throughput (transactions per second)')
    plt.grid(True)
    plt.savefig('ethereum_gas_fee_impact.png')
    plt.show()

if __name__ == "__main__":
    main()
