import csv
import time
import matplotlib.pyplot as plt
from config import connect

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
    tx_sent_timestamp = time.time()
    receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    tx_confirmed_timestamp = time.time()
    return txn_hash.hex(), tx_sent_timestamp, tx_confirmed_timestamp

def collect_data(num_transactions):
    transactions_data = []
    transaction_times = []

    for i in range(num_transactions):
        nonce = w3.eth.get_transaction_count(my_address, 'pending')
        try:
            tx_data = send_transaction(nonce)
            transactions_data.append(tx_data)
            tx_sent_timestamp, tx_confirmed_timestamp = tx_data[1], tx_data[2]
            transaction_times.append(tx_confirmed_timestamp - tx_sent_timestamp)
            print(f"Transaction {i + 1}: Time = {tx_confirmed_timestamp - tx_sent_timestamp} seconds, Hash = {tx_data[0]}")
        except ValueError as e:
            if 'nonce too low' in str(e):
                print(f"Nonce too low error for transaction {i + 1}. Retrying...")
            else:
                print(f"Error: {e}")
            transaction_times.append(0)  # Append zero to keep the list consistent
        except Exception as e:
            print(f"Unexpected error: {e}")
            transaction_times.append(0)  # Append zero to keep the list consistent
        time.sleep(1)  # Wait a second before sending the next transaction

    return transactions_data, transaction_times

def write_to_csv(data, transaction_times, filename='tps_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction ID', 'Timestamp Sent', 'Timestamp Confirmed', 'Transaction Time (seconds)'])
        for row, tx_time in zip(data, transaction_times):
            writer.writerow([row[0], row[1], row[2], tx_time])

def main():
    num_transactions = 20  # Number of transactions to send
    transactions_data, transaction_times = collect_data(num_transactions)
    total_transactions = len(transactions_data)

    print(f"Total Transactions: {total_transactions}")

    write_to_csv(transactions_data, transaction_times, 'tps_data.csv')

    plt.figure(figsize=(12, 7))
    plt.plot(range(1, total_transactions + 1), transaction_times, '*-', color='#ff8a22', label='Transaction Time')
    plt.title('Transaction Time Over Time in Ethereum')
    plt.xlabel('Transaction Number')
    plt.ylabel('Transaction Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('ethereum_transaction_time.png')
    plt.show()

if __name__ == "__main__":
    main()
