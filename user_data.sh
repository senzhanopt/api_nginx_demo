#!/bin/bash
set -e

# Update package lists and install dependencies
apt update
apt upgrade -y
apt install -y unzip curl git jq docker.io

# Enable and start Docker
systemctl enable docker
systemctl start docker

# Add default user to docker group
usermod -aG docker ubuntu  # replace 'ubuntu' if your user is different

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
rm -rf awscliv2.zip aws

# Install Docker Compose
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r .tag_name)
curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose