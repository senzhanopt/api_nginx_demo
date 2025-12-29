## Introduction

This repository is to document necessary steps to run `AWS EC2` for `FastAPI` and `MLflow` tracking.

## Public FastAPI

Youtube tutorial: https://www.youtube.com/watch?v=SgSnz7kW-Ko


Create an `EC2` instance with Ubuntu image; download a pem file; and allow SSH, HTTPS, and HTTP in Network Settings.

Following AWS instructions to SSH into the instance and run the following to install `NGINX` and `uv`:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install nginx -y
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.profile
```


Configure NGINX by creating a config file:
```bash
sudo vim /etc/nginx/sites-available/fastapi_nginx
```

Include:
```bash
server {
    listen 80;
    server_name <YOUR_EC2_PUBLIC_IP>;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

If limiting access, add above `proxy_pass`:
```bash
allow <YOUR_PUBLIC_IP>;
deny all;
```

Test and run NGINX:
```bash
sudo ln -s /etc/nginx/sites-available/fastapi_nginx /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```


Clone this repository and install dependencies:

```bash
git clone https://github.com/senzhanopt/api_nginx_demo.git
cd api_nginx_demo
uv sync
```

Run FastAPI with Uvicorn:
```bash
uv run uvicorn app.main:app
```

Visit http://<YOUR_EC2_PUBLIC_IP>/ for response.

## Optional: Run FastAPI as a systemd Service (skip running uvicorn in the shell)

Create a service file:

```bash
sudo vim /etc/systemd/system/fastapi.service
```

Include:
```bash
[Unit]
Description=FastAPI App with uv
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/api_nginx_demo
ExecStart=/home/ubuntu/.local/bin/uv run uvicorn main:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
sudo systemctl status fastapi
```

## MLflow

Follow the same procedure, and use port 5000 for MLflow by default. Run MLflow server by:
```bash
uv run mlflow server --host 127.0.0.1 --port 5000
```

SSH tunnel to view MLflow server locally at http://localhost:8080:
```bash
ssh -L 8080:localhost:5000 -i your-key.pem ubuntu@your-ec2-ip
```

Note: avoid use MLflow version 3.8.0, which gives an empty UI. See discussion https://github.com/mlflow/mlflow/issues/19592

This stores metadata and artifacts locally.

## HTTPS

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d mlflow.example.com
```

Note: AWS EC2 public DNS (e.g., ec2-13-53-138-24.eu-north-1.compute.amazonaws.com) **cannot be used with Let’s Encrypt**. Use a domain you control.

## MLflow with PostgreSQL and S3

Follow steps in AWS Console to create a S3 bucket. Use a unique bucket name. Block all public access and use default settings.

Creat an IAM role for EC2 with AmazonS3FullAccess policy. Attach the role to the EC2 instance under EC2 instance Actions -> Security -> Modify IAM role.

Test S3 bucket access by:
```bash
sudo apt install awscli -y
aws --version
aws s3 ls
```

Create a PostgreSQL database with Easy create. Give it a DB instance identifier (which is not the database name), master username and self managed password. Set up EC2 connection to the created EC2 instance.

Test access. Use postgres as the default DB_NAME. Give your passward.
```bash
sudo apt install postgresql-client -y
psql -h RDS_ENDPOINT -U USERNAME -d DB_NAME
```

Create a new database for MLflow by:
```bash
CREATE DATABASE mlflow_db;
\q # leave
```

Run MLflow server by:
```bash
uv run mlflow server --backend-store-uri postgresql://<username>:<password>@<rds-endpoint>:5432/<database> --artifacts-destination s3://<s3-bucket> --host 127.0.0.1 --port 5000
```

Check https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/.

Now you are running to run your experiments with MLflow locally by setting the `tracking_uri` as the public DNS or IPv4 address of your EC2 instance.