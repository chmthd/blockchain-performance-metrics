import subprocess
import time
import matplotlib.pyplot as plt
from config import FROM, TO, AMOUNT

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip()

def send_transaction(FROM, TO, amount):
    tx_command = f'lotus send --from {FROM} {TO} {amount}'
    start_time = time.time()
    run_command(tx_command)
    end_time = time.time()
    return start_time, end_time

def collect_data(FROM, TO, amount, num_transactions):
    times = []
    for _ in range(num_transactions):
        start_time, end_time = send_transaction(FROM, TO, amount)
        times.append((end_time - start_time))
    return times

def main():
    offered_loads = [10, 50, 100, 200, 500, 1000]
    throughputs = []

    for load in offered_loads:
        times = collect_data(FROM, TO, AMOUNT, load)
        total_time = sum(times)
        throughput = load / total_time
        throughputs.append(throughput)
        print(f"Offered Load: {load}, Throughput: {throughput} transactions per second")

    plt.figure(figsize=(10, 6))
    plt.plot(offered_loads, throughputs, 'o-', color='#217eff', label='Throughput vs Offered Load')
    plt.title('Throughput Analysis on Filecoin Local Testnet')
    plt.xlabel('Number of Transactions')
    plt.ylabel('Throughput (transactions per second)')
    plt.xticks(offered_loads) 
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
