import subprocess
import time
import matplotlib.pyplot as plt
import csv

from config import FROM, TO, AMOUNT

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip()

def send_transaction(FROM, TO, amount):
    tx_command = f'lotus send --from {FROM} {TO} {amount}'
    tx_sent_timestamp = time.time()
    run_command(tx_command)
    tx_confirmed_timestamp = time.time()
    return tx_sent_timestamp, tx_confirmed_timestamp

def collect_data(FROM, TO, amount, duration_seconds):
    start_time = time.time()
    transactions_data = []
    transaction_times = []

    while time.time() - start_time < duration_seconds:
        tx_sent_timestamp, tx_confirmed_timestamp = send_transaction(FROM, TO, amount)
        transactions_data.append((tx_sent_timestamp, tx_confirmed_timestamp))
        transaction_times.append(tx_confirmed_timestamp - tx_sent_timestamp)
        time.sleep(0.000001) 

    return transactions_data, transaction_times

def write_to_csv(data, filename='filecoin_transaction_data.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp Sent', 'Timestamp Confirmed'])
        for sent, confirmed in data:
            writer.writerow([sent, confirmed])

def main():
    duration_seconds = 60
    transactions_data, transaction_times = collect_data(FROM, TO, AMOUNT, duration_seconds)
    total_transactions = len(transactions_data)
    throughput = total_transactions / duration_seconds

    print(f"Total Transactions: {total_transactions}, Throughput: {throughput} transactions per second")

    plt.figure(figsize=(12, 7))
    plt.plot(range(1, total_transactions + 1), transaction_times, '*-', color='#217eff', label=f'{throughput:.2f} transactions per second')
    plt.title('Transaction Time Over 60 Seconds on Filecoin Local Network')
    plt.xlabel('Transaction Number')
    plt.ylabel('Transaction Time (s)')
    plt.legend()
    plt.grid(True)
    plt.savefig('filecoin_transaction_time.png')
    plt.show()

if __name__ == "__main__":
    main()
