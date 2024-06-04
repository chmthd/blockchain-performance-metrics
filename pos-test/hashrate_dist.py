from web3 import Web3
import matplotlib.pyplot as plt
from collections import defaultdict

# Connect to Ethereum mainnet or testnet node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8000'))

def fetch_block_miners(block_count=1000):
    latest = w3.eth.get_block('latest').number
    start_block = max(0, latest - block_count + 1)  # Ensure start_block is not negative
    miners = defaultdict(int)

    for block_number in range(start_block, latest + 1):
        block = w3.eth.get_block(block_number)
        miners[block.miner] += 1

    return miners


def plot_hash_distribution(miners):
    labels = list(miners.keys())
    counts = list(miners.values())

    plt.figure(figsize=(10, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%')
    plt.title('Hash Rate Distribution Among Miners')
    plt.show()

def main():
    try:
        miners = fetch_block_miners()
        if miners:
            plot_hash_distribution(miners)
        else:
            print("No miners found or no blocks mined yet.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

