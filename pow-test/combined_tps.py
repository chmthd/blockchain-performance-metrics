import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
file_3node = "/home/c/Documents/consensus/pow-test/metrics/tps/tps_load/3node.csv"
file_9node = "/home/c/Documents/consensus/pow-test/metrics/tps/tps_load/9node.csv"
file_27node = "/home/c/Documents/consensus/pow-test/metrics/tps/tps_load/27node.csv"

data_3node = pd.read_csv(file_3node)
data_9node = pd.read_csv(file_9node)
data_27node = pd.read_csv(file_27node)
# data_27node = pd.read_csv(file_27node)

loads = [5, 50, 100, 200, 500, 1000]

# Calculate throughput for each load
def calculate_throughput(data, loads):
    throughputs = []
    for load in loads:
        subset = data.head(load)
        start_time = subset['Timestamp Sent'].min()
        end_time = subset['Timestamp Confirmed'].max()
        duration = end_time - start_time
        throughput = load / duration
        throughputs.append(throughput)
    return throughputs

tps_3node = calculate_throughput(data_3node, loads)
tps_9node = calculate_throughput(data_9node, loads)
tps_27node = calculate_throughput(data_27node, loads)

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(loads, tps_3node, label='3 Nodes', color='#2B80D4', marker='o')
plt.plot(loads, tps_9node, label='9 Nodes', color='#D42B80', marker='o')
plt.plot(loads, tps_27node, label='27 Nodes', color='#80D42B', marker='o')
plt.xlabel('Number of Transactions')
plt.ylabel('Throughput (transactions per second)')
plt.title('Impact of Load Variation on Transaction Throughput in Bitcoin RegTest')
plt.legend()
plt.grid(True)
plt.show()
