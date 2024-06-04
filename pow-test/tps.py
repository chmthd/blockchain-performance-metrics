import csv
import time
import concurrent.futures
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
    except Exception as e:
        return str(e), time.time(), time.time()

def collect_data(num_transactions):
    mining_address = rpc_connection.getnewaddress()
    rpc_connection.generatetoaddress(101, mining_address)
    transactions_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_transaction, i) for i in range(num_transactions)]
        for future in concurrent.futures.as_completed(futures):
            transactions_data.append(future.result())

    return transactions_data

def write_to_csv(data, filename='tps_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction ID', 'Timestamp Sent', 'Timestamp Confirmed'])
        for row in data:
            writer.writerow(row)

def main():
    global rpc_connection
    rpc_connection = connect()

    offered_loads = [5, 50, 100, 200, 500, 1000] 
    throughputs = []
    all_transactions_data = []

    for load in offered_loads:
        transactions_data = collect_data(load)
        all_transactions_data.extend(transactions_data)  # Collect all data in a single list
        total_time = max([tx[2] for tx in transactions_data]) - min([tx[1] for tx in transactions_data])
        throughput = load / total_time
        throughputs.append(throughput)
        print(f"Offered Load: {load}, Throughput: {throughput} transactions per second")

    # Write all data to a single CSV file
    write_to_csv(all_transactions_data, 'tps_data.csv')

    plt.figure(figsize=(12, 7))
    plt.plot(offered_loads, throughputs, 'o-', color='#ff8a22', label='Throughput vs Offered Load')
    plt.title('Impact of Load Variation on Transaction Throughput in Bitcoin RegTest using 9 Nodes')
    plt.xlabel('Number of Transactions')
    plt.ylabel('Throughput (transactions per second)')
    plt.xticks(offered_loads)
    plt.legend()
    plt.grid(True)
    plt.savefig('bitcoin_throughput.png')
    plt.show()

if __name__ == "__main__":
    main()

