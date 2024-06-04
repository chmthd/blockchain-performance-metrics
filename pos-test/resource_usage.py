import psutil
import time
import matplotlib.pyplot as plt
import matplotlib as mpl  # Make sure matplotlib is imported as mpl

def monitor_resources(interval=10, duration=60):
    """ Monitor and log system resources at specified intervals for a given duration. """
    # Define lists to store the data
    times = []
    cpu_usages = []
    memory_usages = []
    disk_reads = []
    disk_writes = []
    net_sent = []
    net_received = []

    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        current_time = time.time() - start_time
        cpu = psutil.cpu_percent() 
        memory = psutil.virtual_memory().percent
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()

        # Append data to lists
        times.append(current_time)
        cpu_usages.append(cpu)
        memory_usages.append(memory)
        disk_reads.append(disk_io.read_bytes / 1024)  # Convert to KB
        disk_writes.append(disk_io.write_bytes / 1024)  # Convert to KB
        net_sent.append(net_io.bytes_sent / 1024)  # Convert to KB
        net_received.append(net_io.bytes_recv / 1024)  # Convert to KB

        time.sleep(interval)

    # Set the plot style within a context manager
    with mpl.rc_context({'lines.linewidth': 2, 'lines.linestyle': ':'}):
        plt.figure(figsize=(10, 8))
        colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan']

        # Plot the data
        plt.plot(times, cpu_usages, label='CPU Usage (%)', color=colors[0], marker='.')
        plt.plot(times, memory_usages, label='Memory Usage (%)', color=colors[1], marker='.')
        plt.plot(times, disk_reads, label='Disk Read (KB)', color=colors[2], marker='.')
        plt.plot(times, disk_writes, label='Disk Write (KB)', color=colors[3], marker='.')
        plt.plot(times, net_sent, label='Network Sent (KB)', color=colors[4], marker='.')
        plt.plot(times, net_received, label='Network Received (KB)', color=colors[5], marker='.')

        # Set the titles and labels
        plt.title('Resource Usage Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Usage (CPU & Memory in %, Disk & Network in KB)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# This block makes sure the script only executes when run directly (not imported as a module)
if __name__ == "__main__":
    monitor_resources(interval=10, duration=600) 

