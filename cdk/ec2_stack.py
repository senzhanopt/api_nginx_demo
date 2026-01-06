from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct
from pathlib import Path


class Ec2FastApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # VPC
        vpc = ec2.Vpc(
            self,
            "SimpleVpc",
            max_azs=2,
            nat_gateways=1,
        )

        # Security Group: SSH + HTTP open
        sg = ec2.SecurityGroup(
            self,
            "FastApiEC2SG",
            vpc=vpc,
            description="Allow SSH and HTTP",
            allow_all_outbound=True,
        )

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="SSH access",
        )

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="HTTP access",
        )

        # IAM Role for EC2 with ECR access
        role = iam.Role(
            self,
            "FastApiEC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )

        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonEC2ContainerRegistryReadOnly"
            )
        )

        # Ubuntu AMI (latest LTS)
        ubuntu_ami = ec2.MachineImage.lookup(
            name="ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*",
            owners=["099720109477"],  # Canonical
        )

        # EC2 Instance
        instance = ec2.Instance(
            self,
            "FastApiInstance",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ubuntu_ami,
            security_group=sg,
            role=role,
            key_name="fastapidemo",
        )

        # -----------------------------
        # USER DATA
        # -----------------------------
        # Read user_data.sh from parent folder
        user_data = Path(__file__).resolve().parent.parent / "user_data.sh"
        instance.add_user_data(user_data.read_text())

        # Add this right after creating the instance
        CfnOutput(
            self,
            "FastApiPublicIp",
            value=instance.instance_public_ip,
            description="Public IPv4 address of the FastAPI EC2 instance",
        )
