# Real-Time Crypto Streaming Analytics Platform

## Project Overview

This project is a production-grade real-time data engineering and streaming analytics platform designed to demonstrate modern cloud-native data infrastructure and distributed systems engineering.

The platform ingests live cryptocurrency market data from external APIs, streams the events through Apache Kafka, processes and transforms the data using Apache Spark Structured Streaming, stores processed analytics in PostgreSQL, and exposes real-time analytics through a FastAPI service.

The system also includes workflow orchestration with Apache Airflow, monitoring with Prometheus and Grafana, Dockerized services, Kubernetes manifests, Terraform infrastructure provisioning, and AWS EKS deployment preparation.

---

# System Architecture

```text
Crypto API
    ↓
Kafka Producer
    ↓
Apache Kafka
    ↓
Spark Structured Streaming
    ↓
PostgreSQL
    ↓
FastAPI Analytics API
    ↓
Redis Cache
    ↓
Prometheus + Grafana Monitoring
    ↓
Kubernetes / AWS EKS
    ↓
Terraform Infrastructure
    ↓
GitHub Actions CI/CD
```

---

# Technologies Used

## Backend & APIs

* FastAPI
* Python 3.11

## Streaming & Data Engineering

* Apache Kafka
* Apache Spark Structured Streaming
* Apache Airflow

## Databases & Caching

* PostgreSQL
* Redis

## Monitoring & Observability

* Prometheus
* Grafana
* CloudWatch (AWS)

## Infrastructure & DevOps

* Docker
* Docker Compose
* Kubernetes
* Terraform
* AWS EKS
* AWS ECR
* GitHub Actions

---

# Features

* Real-time crypto market data ingestion
* Kafka event streaming pipeline
* Distributed Spark processing
* PostgreSQL analytics storage
* Redis caching layer
* FastAPI analytics API
* Prometheus metrics endpoint
* Grafana dashboards
* Apache Airflow DAG orchestration
* Kubernetes deployments and services
* Horizontal Pod Autoscaling (HPA)
* Ingress configuration
* Terraform AWS infrastructure provisioning
* GitHub Actions CI/CD pipelines
* Production-style project structure

---

# Project Structure

```text
crypto-streaming-platform/
│
├── api/
├── producer/
├── streaming/
├── airflow/
├── infra/
├── k8s/
├── monitoring/
├── docs/
├── .github/workflows/
├── docker-compose.yml
├── README.md
└── .env.example
```

---

# API Endpoints

## Root Endpoint

```http
GET /
```

## Health Check

```http
GET /health
```

## Latest Prices

```http
GET /prices/latest
```

## Symbol Price History

```http
GET /prices/{symbol}
```

Example:

```http
GET /prices/bitcoin
```

## Top Movers Analytics

```http
GET /analytics/top-movers
```

## Average Price Analytics

```http
GET /analytics/average-price/{symbol}
```

## Prometheus Metrics

```http
GET /metrics
```

---

# Local Development Setup

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/crypto-streaming-platform.git
cd crypto-streaming-platform
```

## Start Full Platform

```bash
docker compose up --build
```

---

# Local Service URLs

| Service      | URL                        |
| ------------ | -------------------------- |
| FastAPI      | http://localhost:8000      |
| Swagger Docs | http://localhost:8000/docs |
| Prometheus   | http://localhost:9090      |
| Grafana      | http://localhost:3000      |
| Airflow      | http://localhost:8080      |

---

# Grafana Credentials

```text
Username: admin
Password: admin
```

---

# Airflow Credentials

```text
Username: admin
Password: admin
```

---

# Kubernetes Components

* Namespace
* Deployments
* StatefulSets
* Services
* ConfigMaps
* Secrets
* Horizontal Pod Autoscaler
* Ingress
* Health Checks

---

# Terraform Infrastructure

Terraform provisions:

* AWS VPC
* AWS EKS Cluster
* ECR Repositories
* CloudWatch Log Groups
* Managed Node Groups

---

# CI/CD Pipeline

GitHub Actions pipelines include:

* Docker image builds
* Terraform validation
* Kubernetes YAML validation
* AWS authentication
* EKS configuration
* Deployment preparation

---

# Monitoring

Prometheus collects application metrics from FastAPI.

Grafana visualizes:

* API request metrics
* System health
* Streaming activity
* Pipeline monitoring

---

# Future Improvements

* Managed Kafka using Amazon MSK
* Helm charts
* ArgoCD GitOps deployment
* Distributed Spark cluster
* Real-time anomaly detection
* WebSocket streaming API
* ML-based price prediction
* Multi-region deployment

---

# Screenshots

Add screenshots for:

* Kafka streaming logs
* Spark processing
* PostgreSQL records
* FastAPI Swagger UI
* Grafana dashboards
* Airflow DAG execution
* Kubernetes pods
* GitHub Actions pipeline
* Terraform apply output
* AWS EKS cluster

---

# Author

Ayesha Najib

---

# License

This project is for educational and portfolio purposes.
