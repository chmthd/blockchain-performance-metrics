import subprocess
import time
import concurrent.futures
import matplotlib.pyplot as plt

def run_command(command):
    """Run shell commands and capture the output."""
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        raise Exception(f"Command Error: {result.stderr.strip()}")
    return result.stdout.strip()

def send_transaction(from_address, to_address, amount, nonce):
    """Send a transaction using the Lotus CLI and measure the latency."""
    tx_command = f"lotus send --from {from_address} --to {to_address} --value {amount} --nonce {nonce}"
    tx_sent_timestamp = time.time()
    run_command(tx_command)
    tx_confirmed_timestamp = time.time()
    latency = tx_confirmed_timestamp - tx_sent_timestamp
    return latency


def get_nonce(from_address):
    """Get the current highest nonce for the given address."""
    # Use jq to select nonces, return 0 if null, and get the maximum or 0 if none.
    nonce_command = f"lotus mpool pending --from {from_address} | jq -r '[.[] | .Message.Nonce // 0] | max // 0'"
    result = run_command(nonce_command)
    # Ensure the result is a digit and return it, else return 0.
    return int(result.strip()) if result.strip().isdigit() else 0


def collect_data(from_address, to_address, amount, num_parallel_requests):
    nonce = get_nonce(from_address)  # Correctly get the starting nonce
    latencies = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Correctly schedule send_transaction calls
        futures = [executor.submit(send_transaction, from_address, to_address, amount, nonce + i) for i in range(num_parallel_requests)]
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

def main():
    from_address = 't3w7o342fj7ekvaepqsh2epmadwuqk7m76luzm3gj44bo5rzxx3fg7muuyukpgc4znoiopc7sn4d25cyf36w5a'
    to_address = 't1imnmmnph756glnsph6nfhf5ozuqesfqkoa4gkoy'
    amount = '0.001'  # Small FIL amount for testing
    parallel_requests = [1, 10, 20, 30, 40, 50]
    all_latencies = []

    for num_requests in parallel_requests:
        latencies = collect_data(from_address, to_address, amount, num_requests)
        all_latencies.append(latencies)
        time.sleep(10)  # Delay between tests to prevent nonce overlap and rate limit issues

    plot_latencies(parallel_requests, all_latencies)

if __name__ == "__main__":
    main()
