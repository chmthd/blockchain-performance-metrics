import csv
import time
import random
import matplotlib.pyplot as plt
from config import connect, RECIPIENT_ADDRESS
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def send_transaction(nonce):
    rpc_connection = connect()
    try:
        txid = rpc_connection.sendtoaddress(RECIPIENT_ADDRESS, 0.01)
        tx_sent_timestamp = time.time()
        tx_info = rpc_connection.gettransaction(txid)
        while 'confirmations' not in tx_info or tx_info['confirmations'] < 1:
            time.sleep(0.5)
            tx_info = rpc_connection.gettransaction(txid)
        tx_confirmed_timestamp = time.time()
        return txid, tx_sent_timestamp, tx_confirmed_timestamp
    except JSONRPCException as e:
        return str(e), time.time(), time.time()
    finally:
        rpc_connection = None

def collect_data(duration_seconds):
    start_time = time.time()
    transactions_data = []
    transaction_times = []

    while time.time() - start_time < duration_seconds:
        tx_data = send_transaction(len(transactions_data) + 1)
        transactions_data.append(tx_data)
        tx_sent_timestamp, tx_confirmed_timestamp = tx_data[1], tx_data[2]
        transaction_times.append(tx_confirmed_timestamp - tx_sent_timestamp)
        time.sleep(5)

    return transactions_data, transaction_times

def write_to_csv(data, transaction_times, filename='tps_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction ID', 'Timestamp Sent', 'Timestamp Confirmed', 'Transaction Time (seconds)'])
        for row, tx_time in zip(data, transaction_times):
            writer.writerow([row[0], row[1], row[2], tx_time])

def main():
    global rpc_connection
    rpc_connection = connect()
    duration_seconds = 600  # Extended duration to 10 minutes to observe block mining effect
    transactions_data, transaction_times = collect_data(duration_seconds)
    total_transactions = len(transactions_data)
    throughput = total_transactions / duration_seconds

    print(f"Total Transactions: {total_transactions}, Throughput: {throughput} transactions per second")
    write_to_csv(transactions_data, transaction_times, 'tps_data.csv')

    plt.figure(figsize=(12, 7))
    plt.plot(range(1, total_transactions + 1), transaction_times, '*-', color='#ff8a22', label='Transaction Time')
    plt.title('Transaction Time Over Time in Bitcoin RegTest')
    plt.xlabel('Transaction Number')
    plt.ylabel('Transaction Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('bitcoin_transaction_time.png')
    plt.show()

if __name__ == "__main__":
    main()
