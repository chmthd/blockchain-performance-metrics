import csv
import time
import concurrent.futures
import matplotlib.pyplot as plt
from config import connect, RECIPIENT_ADDRESS
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Send a transaction on Bitcoin RegTest
def send_transaction(nonce):
    rpc_connection = connect()
    try:
        txid = rpc_connection.sendtoaddress(RECIPIENT_ADDRESS, 0.01)  # Send 0.01 BTC
        tx_sent_timestamp = time.time()

        tx_info = rpc_connection.gettransaction(txid)
        while 'confirmations' not in tx_info or tx_info['confirmations'] < 1:
            time.sleep(0.5)  # Check every 0.5 seconds
            tx_info = rpc_connection.gettransaction(txid)

        tx_confirmed_timestamp = time.time()
        latency = tx_confirmed_timestamp - tx_sent_timestamp
        return latency
    except JSONRPCException as e:
        return float('inf')  # Return infinity for failed transactions

# Collect data from multiple transactions
def collect_data(num_parallel_requests):
    latencies = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_transaction, i) for i in range(num_parallel_requests)]
        for future in concurrent.futures.as_completed(futures):
            latency = future.result()
            if latency != float('inf'):  # Exclude failed transactions
                latencies.append(latency)

    return latencies

# Plot latencies
def plot_latencies(parallel_requests, latencies):
    plt.figure(figsize=(12, 8))
    for i, latency in enumerate(latencies):
        plt.scatter([parallel_requests[i]]*len(latency), latency, label=f'{parallel_requests[i]} requests')

    plt.title('Network Latency Across Different Batch Sizes')
    plt.xlabel('Number of Requests')
    plt.ylabel('Latency (s)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Save latencies to CSV
def save_latencies_to_csv(parallel_requests, latencies, filename='latencies.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number of Requests', 'Latency (s)'])

        for i, latency_batch in enumerate(latencies):
            for latency in latency_batch:
                writer.writerow([parallel_requests[i], latency])

# Main function to run the test
def main():
    parallel_requests = [1, 10, 50, 100, 500, 1000]
    all_latencies = []

    for num_requests in parallel_requests:
        latencies = collect_data(num_requests)
        all_latencies.append(latencies)
        time.sleep(10)  # Wait for 10 seconds between tests

    plot_latencies(parallel_requests, all_latencies)
    save_latencies_to_csv(parallel_requests, all_latencies)

if __name__ == "__main__":
    main()
