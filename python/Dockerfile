FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3 \
    python3-pip \
    git \
    vim

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo install dora-cli --locked && pip install dora-rs

RUN rustc --version && \
    cargo --version && \
    python3 --version && \
    pip3 --version

WORKDIR /app

CMD ["/bin/bash"]