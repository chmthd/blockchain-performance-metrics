import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV files
file_3node = '/home/c/Documents/consensus/pos-test/metrics/fees/3node.csv'
file_9node = '/home/c/Documents/consensus/pos-test/metrics/fees/9node.csv'
file_27node = '/home/c/Documents/consensus/pos-test/metrics/fees/27node.csv'

data_3node = pd.read_csv(file_3node)
data_9node = pd.read_csv(file_9node)
data_27node = pd.read_csv(file_27node)

# Get the unique gas prices for setting x-axis ticks
gas_prices = sorted(set(data_3node['Gas Price (gwei)']).union(data_9node['Gas Price (gwei)'], data_27node['Gas Price (gwei)']))

# Plot the data
plt.figure(figsize=(12, 6))

plt.plot(data_3node['Gas Price (gwei)'], data_3node['Throughput (transactions per second)'], label='3 Nodes', color='#26D9A1', marker='o')
plt.plot(data_9node['Gas Price (gwei)'], data_9node['Throughput (transactions per second)'], label='9 Nodes', color='#A126D9', marker='o')
plt.plot(data_27node['Gas Price (gwei)'], data_27node['Throughput (transactions per second)'], label='27 Nodes', color='#D9A126', marker='o')

plt.xlabel('Gas Price (gwei)')
plt.ylabel('Throughput (transactions per second)')
plt.title('Impact of Gas Price on Transaction Throughput in PoS')
plt.legend()
plt.grid(True)

# Set the x-axis ticks to show the exact gas prices used in your data
plt.xticks(gas_prices)

plt.savefig('combined_pos_throughput.png')
plt.show()
