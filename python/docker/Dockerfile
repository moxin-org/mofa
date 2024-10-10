FROM arm64v8/ubuntu:22.04

# 设置环境变量以非交互模式安装
ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|https://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com/ubuntu/|https://repo.huaweicloud.com/ubuntu/|g' /etc/apt/sources.list


RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y vim wget lsof  curl uuid-dev python3.10 python3.10-distutils python3.10-venv  git && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置默认 Python 版本
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# 安装 Rust 和 Cargo
RUN apt-get update && apt-get install -y curl && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    /root/.cargo/bin/rustup default stable

# 将 Cargo 的 bin 目录添加到 PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# 确认 Rust 和 Cargo 安装成功
RUN rustc --version && cargo --version

# 安装 dora-cli 和 dora-rs
RUN cargo install dora-cli --locked && \
    pip3 install dora-rs

# 验证 Python 版本
RUN python3 --version
RUN mkdir -p /project && \
    cd /project && \
    git clone https://github.com/moxin-org/mofa.git && \
    cd mofa && \
    cd /project/mofa/python && \
    pip3 install --upgrade pip --index-url https://pypi.org/simple && \
    pip3 install --upgrade --ignore-installed blinker && \
    pip3 install -e .  && \
    cd /project/mofa/python/mofa/agent_templates/reasoner && \
    dora build reasoner_dataflow.yml


WORKDIR /project

#RUN apt-get update -y && \
#    apt-get install -y --no-install-recommends \
#        build-essential \
#        git \
#        vim \
#        cmake \
#        uuid-dev \
#        libssl-dev \
#        python3-dev \
#        make \
#        wget \
#        lsof \
#        curl && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
#
#
#RUN cd /project && \
#    git clone https://github.com/xlang-foundation/xMind.git && \
#    cd xMind/ThirdParty && \
#    git clone https://github.com/xlang-foundation/xlang.git && \
#    cd xlang && \
#    echo "Switched to Jit branch successfully." && \
#    cd /project/xMind && \
#    mkdir -p out && \
#    echo "Created build directory successfully."
#
#
#RUN cd /project/xMind/out && \
#    cmake  .. && \
#    make -j$(nproc)
#
#
## 复制 micromamba-2.0.0-1.tar.bz2 到镜像中
#COPY micromamba-2.0.0-1.tar.bz2 /project/
#
## 安装 micromamba
#RUN mkdir -p /project/bin && \
#    tar -xvjf /project/micromamba-2.0.0-1.tar.bz2 -C /project/bin --strip-components=1 && \
#    chmod +x /project/bin/micromamba
#
## 创建 micromamba 环境并安装依赖项
#RUN /project/bin/micromamba create -p /opt/conda -y && \
#    /project/bin/micromamba install -p /opt/conda xeus xeus-zmq cmake zeromq cppzmq openssl xtl nlohmann_json -c conda-forge -y && \
#    /project/bin/micromamba clean --all --yes
#
## 设置环境变量
## ENV PATH=/opt/conda/bin:$PATH
#ENV PATH=/project/bin:/opt/conda/bin:$PATH
#ENV CMAKE_PREFIX_PATH=/opt/conda
#ENV LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
#
#
## 构建 xeus-xlang
#RUN git clone https://gitcode.com/wt2k/xeus-xlang.git && \
#    cd xeus-xlang && \
#    mkdir build && cd build && \
#    cmake .. && \
#    make -j$(nproc) && \
#    make install
#RUN cp -r /project/xeus-xlang/install/share ~/.local
#COPY update_xlang_env.sh /project/

CMD ["/bin/bash"]
