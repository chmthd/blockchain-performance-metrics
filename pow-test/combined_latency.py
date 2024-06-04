import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
df_3node = pd.read_csv('/home/c/Documents/consensus/pow-test/metrics/latency/3node.csv')
df_9node = pd.read_csv('/home/c/Documents/consensus/pow-test/metrics/latency/9node.csv')
df_27node = pd.read_csv('/home/c/Documents/consensus/pow-test/metrics/latency/27node.csv')

# Define the batch sizes for plotting
batch_sizes = [1, 10, 50, 100, 500, 1000]

# Aggregate the data by batch size and calculate the mean latency
agg_3node = df_3node.groupby('Number of Requests')['Latency (s)'].mean().reset_index()
agg_9node = df_9node.groupby('Number of Requests')['Latency (s)'].mean().reset_index()
agg_27node = df_27node.groupby('Number of Requests')['Latency (s)'].mean().reset_index()

plt.figure(figsize=(12, 8))

plt.plot(agg_3node['Number of Requests'], agg_3node['Latency (s)'], marker='o',color='#2B80D4', label='3 Nodes')
plt.plot(agg_9node['Number of Requests'], agg_9node['Latency (s)'], marker='o',color='#D42B80', label='9 Nodes')
plt.plot(agg_27node['Number of Requests'], agg_27node['Latency (s)'], marker='o', color='#80D42B', label='27 Nodes')

plt.title('Network Latency Across Different Batch Sizes')
plt.xlabel('Number of Requests')
plt.ylabel('Latency (s)')
plt.legend()
plt.grid(True)
plt.show()
