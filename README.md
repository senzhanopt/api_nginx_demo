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
uv run uvicorn main:app
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