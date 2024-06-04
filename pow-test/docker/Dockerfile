# Use an official Ubuntu base image
FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y wget

# Set Bitcoin Core version
ARG BITCOIN_VERSION=27.0
ARG BITCOIN_URL=https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/bitcoin-${BITCOIN_VERSION}-x86_64-linux-gnu.tar.gz

# Download, unpack and install Bitcoin Core
RUN wget ${BITCOIN_URL} -O bitcoin.tar.gz && \
    tar -xzvf bitcoin.tar.gz -C /usr/local --strip-components=1 --exclude=*-qt

# Cleanup
RUN rm bitcoin.tar.gz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

# Ensure the Bitcoin data directory exists
RUN mkdir -p /root/.bitcoin

# Expose ports for Bitcoin
EXPOSE 18443 18444

# Start Bitcoin Core
CMD ["bitcoind", "-printtoconsole"]

