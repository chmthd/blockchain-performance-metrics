import time
import concurrent.futures
import matplotlib.pyplot as plt
from web3 import Web3, Account
from config import connect, PRIVATE_KEY, RECIPIENT_ADDRESS


w3 = connect()
acct = Account.from_key(PRIVATE_KEY)

def send_transaction_and_measure_finality(nonce, confirmations=6):
    """Send a transaction and measure the time to achieve finality."""
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
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    while True:
        current_block = w3.eth.block_number
        if current_block >= tx_receipt.blockNumber + confirmations:
            finality_achieved_timestamp = time.time()
            break
        time.sleep(5)
    
    finality_time = finality_achieved_timestamp - tx_sent_timestamp
    return finality_time

def collect_finality_times(num_transactions):
    finality_times = []
    start_nonce = w3.eth.get_transaction_count(acct.address)
    for i in range(num_transactions):
        finality_time = send_transaction_and_measure_finality(start_nonce + i)
        finality_times.append(finality_time)
        print(f"Transaction {i+1}: Confirmation Time = {finality_time:.2f} seconds")
    return finality_times

def plot_finalities(finality_times):
    num_transactions = len(finality_times)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_transactions + 1), finality_times, marker='*', linestyle='--', color='#6e57d2')
    plt.title('Transaction Confirmation Time')
    plt.xlabel('Transaction Number')
    plt.ylabel('Confirmation Time (s)')
    plt.grid(True)
    plt.savefig('finality.png') 
    plt.show()

def main():
    num_transactions = 10 
    finality_times = collect_finality_times(num_transactions)
    plot_finalities(finality_times)

if __name__ == "__main__":
    main()
