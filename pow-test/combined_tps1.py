import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
df_3node = pd.read_csv('/home/c/Documents/consensus/pow-test/metrics/tps/avg_tps/3node.csv')
df_9node = pd.read_csv('/home/c/Documents/consensus/pow-test/metrics/tps/avg_tps/9node.csv')
df_27node = pd.read_csv('/home/c/Documents/consensus/pow-test/metrics/tps/avg_tps/27node.csv')

# Add a 'Transaction Number' column based on the index
df_3node['Transaction Number'] = df_3node.index + 1
df_9node['Transaction Number'] = df_9node.index + 1
df_27node['Transaction Number'] = df_27node.index + 1

# Plot the data from all CSV files on the same graph
plt.figure(figsize=(12, 8))

# Plot for 3 nodes
plt.plot(df_3node['Transaction Number'], df_3node['Transaction Time (seconds)'], marker='*', color='#2B80D4', label='3 Nodes')

# Plot for 9 nodes
plt.plot(df_9node['Transaction Number'], df_9node['Transaction Time (seconds)'], marker='*', color='#D42B80', label='9 Nodes')

# Plot for 27 nodes
plt.plot(df_27node['Transaction Number'], df_27node['Transaction Time (seconds)'], marker='*', color='#80D42B', label='27 Nodes')

plt.title('Transaction Time Over Time in Bitcoin RegTest')
plt.xlabel('Transaction Number')
plt.ylabel('Transaction Time (seconds)')
plt.legend()
plt.grid(True)
plt.savefig('tps1.png')
plt.show()