# AWS Cost and Resource Cleanup

## Cost Notice

This project deploys infrastructure on AWS using Amazon EKS, EC2 worker nodes, Load Balancers, CloudWatch, and supporting networking resources.

These services may generate ongoing AWS charges while running.

Major cost contributors:

* Amazon EKS Control Plane
* EC2 Worker Nodes
* Elastic Load Balancers
* CloudWatch Logs
* Public IP Addresses
* EBS Volumes
* NAT Gateway (if enabled)

## Important

To avoid unnecessary AWS charges, destroy infrastructure immediately after testing or demonstration.

## Destroy Infrastructure

Navigate to the infrastructure folder:

```bash
cd infra
```

Run:

```bash
terraform destroy
```

Confirm when prompted:

```text
yes
```

## Verification

After destruction, verify the following resources are removed:

* EKS Cluster
* EKS Node Groups
* EC2 Instances
* Load Balancers
* CloudWatch Log Groups (optional)
* EBS Volumes
* VPC Resources created by Terraform

## Estimated Cost

A small EKS environment with one worker node may still incur charges while active. Costs vary by region and usage. Always destroy resources when not actively testing.
