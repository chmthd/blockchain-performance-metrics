import time
import csv
import matplotlib.pyplot as plt
from config import connect, RECIPIENT_ADDRESS

def send_transaction_and_measure_finality(rpc_connection, nonce, confirmations=6):
    """Send a transaction and measure the time to achieve finality."""
    try:
        txid = rpc_connection.sendtoaddress(RECIPIENT_ADDRESS, 0.01)  # Send 0.01 BTC
        tx_sent_timestamp = time.time()

        tx_info = rpc_connection.gettransaction(txid)
        while 'confirmations' not in tx_info or tx_info['confirmations'] < confirmations:
            time.sleep(1)  # Check every 1 second
            tx_info = rpc_connection.gettransaction(txid)

        finality_achieved_timestamp = time.time()
        finality_time = finality_achieved_timestamp - tx_sent_timestamp
        return (nonce, tx_sent_timestamp, finality_achieved_timestamp, finality_time)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def collect_finality_times(rpc_connection, num_transactions):
    finality_times = []
    for i in range(num_transactions):
        result = send_transaction_and_measure_finality(rpc_connection, i)
        if result is not None:
            finality_times.append(result)
            print(f"Transaction {i+1}: Confirmation Time = {result[3]:.2f} seconds")
    return finality_times

def plot_finalities(finality_times):
    confirmation_times = [x[3] for x in finality_times]
    num_transactions = len(confirmation_times)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_transactions + 1), confirmation_times, marker='*', linestyle='--', color='#ff8a22')
    plt.title('Transaction Confirmation Time')
    plt.xlabel('Transaction Number')
    plt.ylabel('Confirmation Time (s)')
    plt.grid(True)
    plt.savefig('finality.png')
    plt.show()

def write_to_csv(data, filename='finality.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction ID', 'Timestamp Sent', 'Timestamp Confirmed', 'Confirmation Time'])
        for row in data:
            writer.writerow(row)

def main():
    rpc_connection = connect()
    num_transactions = 20
    finality_times = collect_finality_times(rpc_connection, num_transactions)
    plot_finalities(finality_times)
    write_to_csv(finality_times, 'finality.csv')

if __name__ == "__main__":
    main()
