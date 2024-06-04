import subprocess
from config import FROM
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stderr:
        print("Error:", result.stderr)
    return result.stdout.strip()

def get_wallet_balance(FROM):
    balance_command = f'lotus wallet balance {FROM}'
    balance = run_command(balance_command)
    return balance

def get_block_time():
    command = "lotus chain list | head -n 20"
    output = run_command(command)
    # Process the output to calculate the average block time
    return output  # Placeholder for actual block time calculation

def get_num_peers():
    command = "lotus net peers"
    output = run_command(command)
    # Count the number of lines in the output, each representing a peer
    peer_count = len(output.split('\n')) if output else 0
    return peer_count

def main():
    block_time_info = get_block_time()
    num_peers = get_num_peers()
    wallet_address = FROM
    balance = get_wallet_balance(wallet_address)
    print(f"Balance for {wallet_address} is {balance}")
    print(f"Block Time Info: {block_time_info}")
    print(f"Number of Connected Peers: {num_peers}")

if __name__ == "__main__":
    main()
