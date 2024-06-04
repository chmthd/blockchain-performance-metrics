from connection import connect

# Connect to Ethereum node
w3 = connect()
# Check node status
if w3.eth.syncing:
    print("Node is syncing...")
else:
    print("Node is in sync")

# Get the current block number
current_block = w3.eth.block_number
print(f"Current block number: {current_block}")

# Get node version (correcting the method to fetch node info)
node_version = w3.client_version
print(f"Node version: {node_version}")

# Get connected peers count
peer_count = w3.net.peer_count
print(f"Connected peers: {peer_count}")

# Get chain ID
chain_id = w3.eth.chain_id
print(f"Chain ID: {chain_id}")

