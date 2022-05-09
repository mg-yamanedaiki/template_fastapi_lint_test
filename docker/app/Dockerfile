FROM python:3.9.12-slim-buster

WORKDIR /root/app

RUN apt update && \
    apt upgrade -y && \
    apt install --no-install-recommends -y tzdata && \
    apt install -y \
    git \
    build-essential \
    libmariadb-dev \
    default-mysql-client \
    figlet && \
    apt clean

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.create true

RUN apt install -y curl && \
    curl -L https://git.io/dpkg-i-from-url | \
    bash -s -- https://github.com/k1LoW/tbls/releases/download/v1.54.2/tbls_1.54.2-1_amd64.deb
