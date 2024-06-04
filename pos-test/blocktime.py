import time
from web3 import Web3, Account
import matplotlib.pyplot as plt

from config import connect


w3 = connect()

def calculate_block_time(num_blocks):
    times = []
    block_numbers = []

    latest_block = w3.eth.get_block('latest')
    block_numbers.append(latest_block.number)
    times.append(latest_block.timestamp)

    for _ in range(1, num_blocks):
        block = w3.eth.get_block(block_numbers[-1] - 1)
        block_numbers.append(block.number)
        times.append(block.timestamp)

    times.reverse()
    block_times = [t2 - t1 for t1, t2 in zip(times[:-1], times[1:])]
    average_block_time = sum(block_times) / len(block_times)

    return average_block_time, block_times, block_numbers[1:]

def plot_block_times(block_numbers, block_times):
    plt.figure(figsize=(10, 5))
    plt.plot(block_numbers, block_times, marker='o', linestyle='--', color='#6e57d2')
    plt.title('Block Time')
    plt.xlabel('Block Number')
    plt.ylabel('Time Between Blocks (s)')
    plt.grid(True)
    plt.savefig('blocktime.png', format='png')
    plt.show()

def main():
    num_blocks = 100
    average_block_time, block_times, block_numbers = calculate_block_time(num_blocks)
    print(f"Average Block Time: {average_block_time} seconds")
    print(f"Individual Block Times: {block_times}")

    plot_block_times(block_numbers, block_times)

if __name__ == "__main__":
    main()
