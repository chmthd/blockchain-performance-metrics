import csv
import matplotlib.pyplot as plt

# Function to read CSV data
def read_csv_data(filename):
    transaction_numbers = []
    finality_times = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            transaction_numbers.append(int(row[0]))
            finality_times.append(float(row[1]))
    return transaction_numbers, finality_times

# Read data from 3node.csv and 9node.csv
transaction_numbers_3node, finality_times_3node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/finality/3node.csv')
transaction_numbers_9node, finality_times_9node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/finality/9node.csv')
transaction_numbers_27node, finality_times_27node = read_csv_data('/home/c/Documents/consensus/pos-test/metrics/finality/27node.csv')

# Plot the data
plt.figure(figsize=(12, 7))
plt.plot(transaction_numbers_3node, finality_times_3node, 'o-', label='3 Nodes Finality Time', color='#26D9A1', alpha=0.6)
plt.plot(transaction_numbers_9node, finality_times_9node, 'o-', label='9 Nodes Finality Time', color='#A126D9', alpha=0.6)
plt.plot(transaction_numbers_27node, finality_times_27node, 'o-', label='27 Nodes Finality Time', color='#D9A126', alpha=0.6)
plt.title('Transaction Finality Time Over Time (PoS)')
plt.xlabel('Transaction Number')
plt.ylabel('Finality Time (seconds)')
plt.legend()
plt.grid(True)
plt.savefig('combined_pos_finality.png')
plt.show()
