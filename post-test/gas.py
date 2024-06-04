import subprocess
import time
import matplotlib.pyplot as plt
from config import FROM, TO, AMOUNT

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stderr:
        print("Error:", result.stderr)
    return result.stdout.strip()

def send_transaction(from_address, to_address, amount):
    """Send a transaction and return the CID and the timestamps."""
    tx_command = f'lotus send --from {from_address} {to_address} {amount}'
    result = run_command(tx_command)
    end_time = time.time()
    if result:
        # Assuming the result is the CID of the transaction
        return result, end_time
    else:
        return None, end_time

def get_gas_fee(tx_cid):
    """Get the gas fee for a given transaction CID."""
    fee_command = f'lotus state get-msg {tx_cid}'
    result = run_command(fee_command)
    try:
        # Parse the result to find the gas fee
        # This will depend on the actual output format of the 'lotus state get-msg' command
        # Here we assume a hypothetical JSON output which needs to be adjusted to actual output
        json_result = json.loads(result)
        return json_result['Receipt']['GasUsed']
    except (KeyError, ValueError):
        return None


def collect_data(from_address, to_address, amount, num_transactions):
    gas_fees = []
    times = []
    for _ in range(num_transactions):
        tx_cid, end_time = send_transaction(from_address, to_address, amount)
        if tx_cid:
            gas_fee = get_gas_fee(tx_cid)
            if gas_fee is not None:
                gas_fees.append(gas_fee)
        times.append(end_time - time.time())  # Assume start_time is captured within send_transaction
    return times, gas_fees


def main():
    offered_loads = [10, 50, 100, 200, 500, 1000]
    gas_fee_results = []

    for load in offered_loads:
        _, gas_fees = collect_data(FROM, TO, AMOUNT, load)
        average_gas_fee = sum(map(float, gas_fees)) / len(gas_fees)
        gas_fee_results.append(average_gas_fee)
        print(f"Offered Load: {load}, Average Gas Fee: {average_gas_fee}")

    plt.figure(figsize=(10, 6))
    plt.plot(offered_loads, gas_fee_results, 'o-', color='#217eff', label='Average Gas Fee vs Offered Load')
    plt.title('Gas Fee Analysis on Filecoin Local Testnet')
    plt.xlabel('Number of Transactions')
    plt.ylabel('Average Gas Fee (FIL)')
    plt.xticks(offered_loads)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
