version: '3'
services:
  bootnode:
    image: ethereum/client-go:latest
    command: bootnode -nodekeyhex 71dd045d25c7f6c24f4986a525220f4d3ba3ab059b1a8f05e47034d8acd42f65 -verbosity 9 -addr :30310
    ports:
      - "30310:30310"
      - "30310:30310/udp"
  node1:
    image: ethereum/client-go:latest
    volumes:
      - node1:/root/.ethereum
    command: --datadir /root/.ethereum --syncmode 'full' --port 30311 --bootnodes enode://71dd045d25c7f6c24f4986a525220f4d3ba3ab059b1a8f05e47034d8acd42f65@bootnode:30310 --networkid 15 --miner.threads=1 --mine --etherbase '0x0000000000000000000000000000000000000001' --rpc --rpcaddr 0.0.0.0 --rpcport 8501 --rpcapi 'eth,web3,personal,miner'
    ports:
      - "8501:8501"
  node2:
    image: ethereum/client-go:latest
    volumes:
      - node2:/root/.ethereum
    command: --datadir /root/.ethereum --syncmode 'full' --port 30312 --bootnodes enode://71dd045d25c7f6c24f4986a525220f4d3ba3ab059b1a8f05e47034d8acd42f65@bootnode:30310 --networkid 15 --miner.threads=1 --mine --etherbase '0x0000000000000000000000000000000000000002' --rpc --rpcaddr 0.0.0.0 --rpcport 8502 --rpcapi 'eth,web3,personal,miner'
    ports:
      - "8502:8502"

volumes:
  node1:
  node2:

