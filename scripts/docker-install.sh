#!/bin/bash

apt update
apt upgrade -y

# 0. 古いバージョンを削除
apt remove docker docker-engine docker.io containerd runc

# 1. 必要なパッケージをインストール
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 2. GPGキーをシステムに追加
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io

# 3. dockerのグループに現在のユーザーを追加
groupadd docker
usermod -a -G docker $(whoami)


# docker-composeのインストール
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m) -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
