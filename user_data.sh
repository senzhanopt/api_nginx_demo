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

# Clone Github repository into /home/ubuntu
git clone https://github.com/senzhanopt/api_nginx_demo.git /home/ubuntu/api_nginx_demo
cd /home/ubuntu/api_nginx_demo

# Create .env file
cat > .env <<EOF
AWS_ACCOUNT_ID=513689973492
AWS_REGION=eu-north-1
FASTAPI_IMAGE=513689973492.dkr.ecr.eu-north-1.amazonaws.com/fastapi-app:latest
EOF

# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

# Authenticate Docker to AWS ECR using variables from .env
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com