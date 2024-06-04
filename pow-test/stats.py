import subprocess
import re

# Function to run a shell command and return the output
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Docker container name for Bitcoin Core (change this as per your setup)
container_name = "docker-bitcoin-node1-1"

# Get current block number
current_block_number_output = run_command(f"docker exec {container_name} bitcoin-cli -regtest getblockcount")
current_block_number = int(current_block_number_output.strip()) if current_block_number_output.strip() else 0

# Get number of transactions in the mempool
mempool_info = run_command(f"docker exec {container_name} bitcoin-cli -regtest getmempoolinfo")
mempool_transactions_match = re.search(r'"size"\s*:\s*(\d+)', mempool_info)
mempool_transactions = int(mempool_transactions_match.group(1)) if mempool_transactions_match else 0

# Get number of confirmed transactions
# Note: This command needs to be validated as `gettransactioncount` is not a default bitcoin-cli command
# Example: getting wallet transaction count could be done with specific wallet commands or by listing transactions
confirmed_transactions_output = run_command(f"docker exec {container_name} bitcoin-cli -regtest getwalletinfo")
confirmed_transactions_match = re.search(r'"txcount"\s*:\s*(\d+)', confirmed_transactions_output)
confirmed_transactions = int(confirmed_transactions_match.group(1)) if confirmed_transactions_match else 0

# Get number of running nodes
node_count = run_command("docker ps | grep docker-bitcoin-node | wc -l")

# Print results
print("Current Block Number:", current_block_number)
print("No. of Running Nodes:", node_count)
print("No. of Transactions in Mempool:", mempool_transactions)
print("No. of Confirmed Transactions:", confirmed_transactions)

