import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
file_3node = "/home/c/Documents/consensus/pow-test/metrics/finality/3node.csv"
file_9node = "/home/c/Documents/consensus/pow-test/metrics/finality/9node.csv"
file_27node = "/home/c/Documents/consensus/pow-test/metrics/finality/27node.csv"

data_3node = pd.read_csv(file_3node)
data_9node = pd.read_csv(file_9node)
data_27node = pd.read_csv(file_27node)

# Calculate confirmation time
data_3node['Confirmation Time'] = data_3node['Timestamp Confirmed'] - data_3node['Timestamp Sent']
data_9node['Confirmation Time'] = data_9node['Timestamp Confirmed'] - data_9node['Timestamp Sent']
data_27node['Confirmation Time'] = data_27node['Timestamp Confirmed'] - data_27node['Timestamp Sent']

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data_3node.index, data_3node['Confirmation Time'], label='3 Nodes', color='#2B80D4', marker='*')
plt.plot(data_9node.index, data_9node['Confirmation Time'], label='9 Nodes', color='#D42B80', marker='*')
plt.plot(data_27node.index, data_27node['Confirmation Time'], label='27 Nodes', color='#80D42B', marker='*')
plt.xlabel('Transaction Index')
plt.ylabel('Confirmation Time (seconds)')
plt.title('Transaction Confirmation Time Comparison')
plt.legend()
plt.grid(True)
plt.show()