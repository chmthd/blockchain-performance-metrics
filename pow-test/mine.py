import time
import sys
import logging
from config import connect, MY_ADDRESS
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def get_rpc_connection():
    try:
        return connect()
    except Exception as e:
        print(f"Error connecting to RPC: {e}")
        return None

logging.basicConfig(filename='mining.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def mine_blocks(num_blocks, address, rpc_connection):
    if num_blocks > 0 and address.strip() != '':
        try:
            rpc_connection.generatetoaddress(num_blocks, address.strip())
            logging.info(f'Block successfully mined to address {address}')
        except Exception as e:
            logging.error(f'Error during block generation: {e}')

def mine_blocks_periodically(interval_minutes, address):
    rpc_connection = get_rpc_connection()
    while True:
        if rpc_connection is None:
            rpc_connection = get_rpc_connection()
        if rpc_connection:
            mine_blocks(1, address, rpc_connection)
            print(f"A block has been mined, coinbase reward to address {address}")
            print(f"The network currently consists of {rpc_connection.getblockcount()} blocks.")
        time.sleep(interval_minutes)
def mine_blocks_on_demand():
    if len(sys.argv) > 1 and sys.argv[1] == 'mine':
        mine_blocks(1, MY_ADDRESS)
    else:
        print("No mining action taken. Waiting for manual trigger.")
def main():
    mine_blocks_periodically(10, MY_ADDRESS)
    mine_blocks_on_demand()


if __name__ == "__main__":
    main()
