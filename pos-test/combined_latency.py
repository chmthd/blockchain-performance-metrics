import csv
import matplotlib.pyplot as plt

# Function to read CSV data
def read_csv_data(filename):
    num_requests = []
    latencies = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            num_requests.append(int(row[0]))
            latencies.append(float(row[1]))
    return num_requests, latencies

# Read data from 3node.csv and 9node.csv
num_requests_3node, latencies_3node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/latency/3node.csv')
num_requests_9node, latencies_9node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/latency/9node.csv')
num_requests_27node, latencies_27node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/latency/27node.csv')
# Plot the data
plt.figure(figsize=(12, 8))
plt.plot(num_requests_3node, latencies_3node, 'o-', color='#26D9A1', label='3 Nodes Latency', alpha=0.6) 
plt.plot(num_requests_9node, latencies_9node, 'o-', color='#A126D9', label='9 Nodes Latency', alpha=0.6)
plt.plot(num_requests_27node, latencies_27node, 'o-', color='#D9A126', label='27 Nodes Latency', alpha=0.6)

plt.scatter(num_requests_3node, latencies_3node, color='#26D9A1')
plt.scatter(num_requests_9node, latencies_9node, color='#A126D9')
plt.scatter(num_requests_27node, latencies_27node, color='#D9A126')
plt.title('Network Latency Across Different Node Setups (PoS)')
plt.xlabel('Number of Requests')
plt.ylabel('Latency (s)')
plt.legend()
plt.grid(True)
plt.savefig('combined_pos_latency.png')
plt.show()
