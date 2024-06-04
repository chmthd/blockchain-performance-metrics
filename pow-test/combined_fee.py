import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Define the file paths
file_3node = "/home/c/Documents/consensus/pow-test/metrics/gas_fees/3node.csv"
file_9node = "/home/c/Documents/consensus/pow-test/metrics/gas_fees/9node.csv"
file_27node = "/home/c/Documents/consensus/pow-test/metrics/gas_fees/27node.csv"

# Load the CSV files
data_3node = pd.read_csv(file_3node)
data_9node = pd.read_csv(file_9node)
data_27node = pd.read_csv(file_27node)
# Define the fee rates
fee_rates = [0.001, 0.005, 0.01, 0.1]

# Ensure that the data length matches the fee rates
assert len(data_3node) == len(fee_rates), "Data length of 3node.csv does not match fee rates length"
assert len(data_9node) == len(fee_rates), "Data length of 9node.csv does not match fee rates length"
assert len(data_27node) == len(fee_rates), "Data length of 27node.csv does not match fee rates length"

# Plot the data
plt.figure(figsize=(12, 6))

# Assuming the columns are 'Gas Fee' and 'Throughput'
plt.plot(data_3node['Fee Rate'], data_3node['Throughput'], label='3 Nodes', color='#2B80D4', marker='o')
plt.plot(data_9node['Fee Rate'], data_9node['Throughput'], label='9 Nodes', color='#D42B80', marker='o')
plt.plot(data_27node['Fee Rate'], data_27node['Throughput'], label='27 Nodes', color='#80D42B', marker='o')

plt.xlabel('Fee Rate (BTC per KB)')
plt.ylabel('Throughput (transactions per second)')
plt.title('Impact of Fee Rate on Transaction Throughput in Bitcoin RegTest ')
plt.legend()
plt.grid(True)
# Set the x-axis ticks to show the exact fee rates
plt.xticks(fee_rates)

plt.show()
