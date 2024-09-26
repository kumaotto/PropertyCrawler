# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# 基本的なシステムパッケージのインストール
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libsqlite3-dev \
    libreadline-dev \
    libffi-dev \
    libbz2-dev \
    ca-certificates \
    bash-completion \
    jq \
    unzip \
    tree \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /workspace

# デフォルトのシェルをbashに設定
SHELL ["/bin/bash", "-c"]

# コンテナ起動時のデフォルトコマンド
CMD ["/bin/bash"]
