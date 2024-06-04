# config.py
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configuration details
RPC_USER = 'test'
RPC_PASSWORD = 'test'
RPC_PORT = '18443'
RPC_HOST = 'localhost'
MY_ADDRESS = 'bcrt1q736sh3cg575xvhpd3lqpsate3zu9l8zql4m2sj'
RECIPIENT_ADDRESS = 'bcrt1qz59my6ppet2l9mztmy4uq05rdu8lzaekhw4gt5'
NUM_BLOCKS = 200

def connect():
    return AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}")
