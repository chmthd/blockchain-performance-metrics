import subprocess
import time
import matplotlib.pyplot as plt
from config import FROM, TO, AMOUNT

def run_command(command):
    """Run shell commands and capture the output."""
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        print(f"Error: {result.stderr.strip()}")
    return result.stdout.strip()

def send_transaction_and_wait_for_finality(from_address, to_address, amount, confirmations=6):
    """Send a transaction using the Lotus CLI and wait for it to achieve finality."""
    tx_command = f'lotus send --from {from_address} {to_address} {amount}'
    tx_hash = run_command(tx_command)
    print(f"Transaction Hash: {tx_hash}")

    if tx_hash:
        tx_sent_timestamp = time.time()
        tx_block_height = None
        while tx_block_height is None:
            # Check if the transaction has been included in a block
            height_command = f"lotus chain getmessage {tx_hash} | jq -r '.BlockHeight // empty'"
            tx_block_height_str = run_command(height_command)
            if tx_block_height_str.isdigit():
                tx_block_height = int(tx_block_height_str)
            else:
                print("Waiting for transaction to be included in a block...")
                time.sleep(5)  # Wait before retrying

        # Now wait for the transaction to achieve finality
        while True:
            current_head_height = int(run_command("lotus chain head | jq -r '.Height'"))
            if current_head_height >= tx_block_height + confirmations:
                finality_achieved_timestamp = time.time()
                break
            time.sleep(5)  # Check every 5 seconds

        finality_time = finality_achieved_timestamp - tx_sent_timestamp
        return finality_time

    return None  # Return None if no transaction hash was obtained

def collect_finality_times(num_transactions, from_address, to_address, amount, confirmations):
    """Collect finality times for a number of transactions."""
    finality_times = []
    for i in range(num_transactions):
        finality_time = send_transaction_and_wait_for_finality(from_address, to_address, amount, confirmations)
        if finality_time is not None:
            finality_times.append(finality_time)
            print(f"Transaction {i+1}: Finality Time = {finality_time:.2f} seconds")
        else:
            print(f"Transaction {i+1}: Failed to send or confirm.")
    return finality_times

def plot_finalities(finality_times):
    """Plot the finality times of transactions."""
    num_transactions = len(finality_times)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_transactions + 1), finality_times, marker='o', linestyle='-', color='#217eff')
    plt.title('Transaction Finality Time')
    plt.xlabel('Transaction Number')
    plt.ylabel('Finality Time (s)')
    plt.grid(True)
    plt.savefig('transaction_finality.png')
    plt.show()

def main():
    num_transactions = 10
    finality_times = collect_finality_times(num_transactions, FROM, TO, AMOUNT, 6)
    plot_finalities(finality_times)

if __name__ == "__main__":
    main()
