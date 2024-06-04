import csv
import time
import concurrent.futures
import matplotlib.pyplot as plt
from config import connect, RECIPIENT_ADDRESS
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def send_transaction(nonce, fee_rate):
    rpc_connection = connect()
    try:
        txid = rpc_connection.sendtoaddress(
            RECIPIENT_ADDRESS, 0.01, "", "", True, True, 1, fee_rate, "CONSERVATIVE"
        )  # Note the added "CONSERVATIVE" as a string for estimate_mode
        tx_sent_timestamp = time.time()

        tx_info = rpc_connection.gettransaction(txid)
        while 'confirmations' not in tx_info or tx_info['confirmations'] < 1:
            time.sleep(1)
            tx_info = rpc_connection.gettransaction(txid)

        tx_confirmed_timestamp = time.time()
        return txid, tx_sent_timestamp, tx_confirmed_timestamp
    except JSONRPCException as e:
        return str(e), time.time(), time.time()
    finally:
        rpc_connection = None

def collect_data(num_transactions, fee_rate):
    mining_address = rpc_connection.getnewaddress()
    rpc_connection.generatetoaddress(101, mining_address)
    transactions_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_transaction, i, fee_rate) for i in range(num_transactions)]
        for future in concurrent.futures.as_completed(futures):
            transactions_data.append(future.result())

    return transactions_data

def write_to_csv(data, filename='transaction_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction ID', 'Timestamp Sent', 'Timestamp Confirmed'])
        for row in data:
            writer.writerow(row)

def write_throughput_to_csv(data, filename='throughput_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fee Rate', 'Throughput'])
        for row in data:
            writer.writerow(row)

def main():
    global rpc_connection
    rpc_connection = connect()

    fee_rates = [0.001, 0.005, 0.01, 0.1]
    all_transactions_data = []
    throughput_data = []

    for fee_rate in fee_rates:
        transactions_data = collect_data(100, fee_rate)
        all_transactions_data.extend(transactions_data)
        total_time = max([tx[2] for tx in transactions_data]) - min([tx[1] for tx in transactions_data])
        throughput = 100 / total_time
        throughput_data.append((fee_rate, throughput))
        print(f"Fee Rate: {fee_rate}, Throughput: {throughput} transactions per second")
    
    # Write all transaction data to a single CSV file
    write_to_csv(all_transactions_data)

    # Write throughput data to a CSV file
    write_throughput_to_csv(throughput_data)

    # Plot the throughput data
    fee_rates = [x[0] for x in throughput_data]
    throughputs = [x[1] for x in throughput_data]
    
    plt.figure(figsize=(15, 7))
    plt.plot(fee_rates, throughputs, marker='o', linestyle='-', color='#ff8a22', label='Throughput vs Fee Rate')
    plt.title('Impact of Fee Rate on Transaction Throughput in Bitcoin RegTest using 3 Nodes')
    plt.xlabel('Fee Rate (BTC per KB)')
    plt.ylabel('Throughput (transactions per second)')
    plt.xticks(fee_rates)
    plt.legend()
    plt.grid(True)
    plt.savefig('bitcoin_fee_analysis.png')
    plt.show()

if __name__ == "__main__":
    main()
