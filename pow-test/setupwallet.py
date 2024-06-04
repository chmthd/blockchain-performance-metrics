from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from config import connect

def create_wallet(wallet_name):
    rpc_connection = connect()
    try:
        return rpc_connection.createwallet(wallet_name, False, False, "", False, True, True)
    except JSONRPCException as e:
        return f"Error creating wallet: {e}"

def get_new_address(wallet_name):
    rpc_connection = connect()
    try:
        rpc_connection.loadwallet(wallet_name)
        return rpc_connection.getnewaddress()
    except JSONRPCException as e:
        return f"Error getting new address: {e}"

def generate_blocks(address, num_blocks=101):
    rpc_connection = connect()
    try:
        return rpc_connection.generatetoaddress(num_blocks, address)
    except JSONRPCException as e:
        return f"Error generating blocks: {e}"

if __name__ == "__main__":
    wallet_name = input("Enter the wallet name: ") 
    new_wallet_result = create_wallet(wallet_name)
    print("Wallet Creation Result:", new_wallet_result)

    if "Error" not in new_wallet_result:
        new_address = get_new_address(wallet_name)
        print("New Address:", new_address)
        
        if "Error" not in new_address:
            block_generation_result = generate_blocks(new_address, 101)
            print("Block Generation Result:", block_generation_result)
