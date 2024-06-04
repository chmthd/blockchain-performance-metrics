FROM ubuntu:22.04

# Set DNS resolver for apt during the build process
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    apt-get update -y && apt-get install -y \
    mesa-opencl-icd \
    ocl-icd-opencl-dev \
    gcc \
    git \
    jq

# Clone the Lotus repository and set it up
RUN git clone https://github.com/filecoin-project/lotus.git /lotus
WORKDIR /lotus
RUN git checkout releases && make 2k && git submodule update --init --recursive

# Fetch parameters and pre-seal
RUN ./lotus fetch-params 2048 && ./lotus-seed pre-seal --sector-size 2KiB --num-sectors 2

# Default command
CMD ["./lotus", "daemon", "--lotus-make-genesis=devgen.car", "--genesis-template=localnet.json"]

