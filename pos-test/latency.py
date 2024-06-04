import csv
import time
import concurrent.futures
import matplotlib.pyplot as plt
from web3 import Web3, Account
from config import connect, PRIVATE_KEY, RECIPIENT_ADDRESS

w3 = connect()
acct = Account.from_key(PRIVATE_KEY)

def send_transaction(w3, acct, nonce):
    tx = {
        'to': RECIPIENT_ADDRESS,
        'value': w3.to_wei(1, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('30', 'gwei'),
        'nonce': nonce,
        'chainId': 32382
    }
    signed_tx = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_sent_timestamp = time.time()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    tx_confirmed_timestamp = time.time()
    latency = tx_confirmed_timestamp - tx_sent_timestamp
    return latency

def collect_data(w3, acct, num_parallel_requests):
    start_nonce = w3.eth.get_transaction_count(acct.address)
    latencies = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_transaction, w3, acct, start_nonce + i) for i in range(num_parallel_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                latencies.append(future.result())
            except Exception as e:
                print(f"An error occurred: {e}")
    return latencies

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

def save_to_csv(parallel_requests, all_latencies, filename='latencies.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number of Requests', 'Latency (s)'])
        for num_requests, latencies in zip(parallel_requests, all_latencies):
            for latency in latencies:
                writer.writerow([num_requests, latency])

def main():
    parallel_requests = [1, 10, 20, 30, 40, 50]
    all_latencies = []

    for num_requests in parallel_requests:
        latencies = collect_data(w3, acct, num_requests)
        all_latencies.append(latencies)
        time.sleep(10)

    plot_latencies(parallel_requests, all_latencies)
    save_to_csv(parallel_requests, all_latencies)

if __name__ == "__main__":
    main()
