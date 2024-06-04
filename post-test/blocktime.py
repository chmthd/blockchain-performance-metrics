import subprocess
import time
import matplotlib.pyplot as plt

def run_command(command):
    """Execute shell command and return the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stderr:
        raise Exception(result.stderr)
    return result.stdout.strip()

def get_latest_block_height():
    """Retrieve the height of the latest block on the chain."""
    height_command = "lotus chain head | jq -r '.Height'"
    height = run_command(height_command)
    return int(height)

def get_block_time(height):
    """Retrieve the timestamp of a block at a given height."""
    time_command = f"lotus chain getblock --height={height} | jq -r '.Timestamp'"
    timestamp = run_command(time_command)
    return int(timestamp)

def calculate_block_times(num_blocks):
    """Calculate the block times for a specified number of blocks."""
    block_times = []
    initial_height = get_latest_block_height()
    
    # We need to wait for enough blocks to be mined
    print(f"Waiting for {num_blocks} blocks to be mined...")
    while get_latest_block_height() < initial_height + num_blocks:
        time.sleep(10)  # Check every 10 seconds
    
    # Collect timestamps of consecutive blocks
    for height in range(initial_height, initial_height + num_blocks):
        if height > initial_height:
            current_time = get_block_time(height)
            previous_time = get_block_time(height - 1)
            block_time = current_time - previous_time
            block_times.append(block_time)
    
    return block_times

def plot_block_times(block_times):
    """Plot block times."""
    plt.figure(figsize=(10, 6))
    plt.plot(block_times, '-o', label='Block Time')
    plt.title('Block Time Analysis on Filecoin Local Testnet')
    plt.xlabel('Block Number')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    num_blocks = 20  # Number of blocks to measure
    block_times = calculate_block_times(num_blocks)
    plot_block_times(block_times)
    average_block_time = sum(block_times) / len(block_times)
    print(f"Average block time: {average_block_time:.2f} seconds")

if __name__ == "__main__":
    main()
