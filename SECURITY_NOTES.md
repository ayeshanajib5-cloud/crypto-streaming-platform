# Security Notes

This project currently focuses on demonstrating a production-style real-time streaming and cloud deployment workflow.

The current Kubernetes deployment uses default namespace-level service account behavior and does not include custom RBAC, dedicated ServiceAccounts, or NetworkPolicy manifests.

The following security enhancements are recommended before using this project in a real production environment:

- Add dedicated Kubernetes ServiceAccounts for each workload
- Add RBAC roles and role bindings with least-privilege access
- Add NetworkPolicies to restrict pod-to-pod communication
- Store secrets in AWS Secrets Manager or External Secrets Operator
- Enable TLS/HTTPS with a custom domain and AWS ACM certificate
- Avoid committing environment files or sensitive credentials
- Rotate any credentials that were previously exposed

This repository should be treated as a portfolio and demonstration project, not a hardened production security baseline.