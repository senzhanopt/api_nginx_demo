import aws_cdk as cdk
from ec2_stack import Ec2FastApiStack
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = cdk.App()
Ec2FastApiStack(app, "Ec2FastApiStack", env=cdk.Environment(
    account=os.getenv("AWS_ACCOUNT_ID"),
    region=os.getenv("AWS_REGION"),
))
app.synth()