import csv
import matplotlib.pyplot as plt

# Function to read CSV data
def read_csv_data(filename):
    times = []
    tps_values = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            times.append(float(row[0]))
            tps_values.append(float(row[1]))
    return times, tps_values

times_3node, tps_3node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/tps/3node.csv')
times_9node, tps_9node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/tps/9node.csv')
times_27node, tps_27node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/tps/27node.csv')

# Plot the data
plt.figure(figsize=(12, 7))
plt.plot(times_3node, tps_3node, marker='o', label='3 Nodes TPS', color='#3DA1C2', alpha=0.6)
plt.plot(times_9node, tps_9node, marker='o', label='9 Nodes TPS', color='#C23DA1', alpha=0.6)
plt.plot(times_27node, tps_27node, marker='o', label='27 Nodes TPS', color='#A1C23D', alpha=0.6)
plt.title('Transaction Throughput Over Time (PoS)')
plt.xlabel('Time (s)')
plt.ylabel('Transactions Per Second (TPS)')
plt.legend()
plt.grid(True)
plt.savefig('combined_pos_tps.png')
plt.show()
