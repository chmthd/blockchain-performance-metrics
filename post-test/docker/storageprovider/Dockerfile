FROM ubuntu:22.04
RUN apt update -y && apt install -y mesa-opencl-icd ocl-icd-opencl-dev gcc git jq
RUN git clone https://github.com/filecoin-project/lotus.git /lotus
WORKDIR /lotus
RUN git checkout releases && make 2k && git submodule update --init --recursive
RUN ./lotus fetch-params 2048 && ./lotus-seed pre-seal --sector-size 2KiB --num-sectors 2
CMD ["./lotus-miner", "run", "--nosync"]

