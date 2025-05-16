# Docker/Kubernetes To-Do List App Deployment

This repository outlines the progress made on the development and deployment of a containerized
FastAPI-based To-Do application using Kubernetes, Docker, and CI/CD pipelines. The system
integrates observability tools such as Prometheus and Grafana, and follows best practices for modern
DevOps workflows including configuration management, persistent storage, and readiness for production
environments.

https://github.com/user-attachments/assets/9e44f0a4-7d2c-4994-8da4-5fdcbd92823d

## Group Members
- 148322 - Kuria Rehema Manuella
- 138982 - Cindy Mugure Gachuhi
- 149264 - Mwaura Margaret Wambui

## Objectives

The main goals of the project were:

- To design Kubernetes manifests for a multi-tier application.
- To implement secure environment configurations using Secrets and ConfigMaps.
- To handle both ephemeral and persistent storage needs within the cluster.
- To scale services and apply service exposure techniques like load balancing.

## Tools and Technologies Used

Kubernetes
kubectl
Minikube (for local cluster setup)
Docker

## Installation Guide

1. Have a running Kubernetes cluster (e.g., Minikube).
2. Clone the repository:

```bash
git clone https://github.com/CindyMG/widgetario-k8s
```
3. Navigate to the directory
```bash
cd 
```

## Project Breakdown

**Part 1: Kubernetes Deployment**
* Successfully containerized:
  FastAPI backend application.
  PostgreSQL database instance.
* Deployed backend and database as Kubernetes Deployments.
* Exposed them via ClusterIP Services.

  **Proof**:
- `k8s/postgres-deployment.yaml`
- `k8s/postgres-service.yaml`
- `Dockerfile`

**Part 2: Configuration Management**
* Used Kubernetes Secrets to secure:
 - PostgreSQL credentials.
 - JWT tokens and private app settings.
* Applied ConfigMaps for non-sensitive configurations such as:
 - Environment variables.
 - JWT expiry settings.
 - Debug/production mode flags

 **Proof**:
- `k8s/secrets.yaml`
- `k8s/configmap.yaml`
- `app/main.py`

**Part 3: Persistent Storage**
* Configured PersistentVolumeClaim (PVC) for PostgreSQL to ensure data persistence across pod restarts and crashes.
* Future volumes (e.g., emptyDir) have been proposed for ephemeral analytics data

**Proof**:
- `k8s/postgres-pvc.yaml`
- `postgres-deployment.yaml` shows volume mounts

**Part 4 - Ingress and DNS Configuration**
* Installed NGINX Ingress Controller.
* Configured domain routing:
 - api.todo.local mapped to the backend FastAPI service.
* Edited the local /etc/hosts file to support local development and testing via custom domain names.

**Proof**:
- `k8s/ingress.yaml`

**Part 5 - Production Readiness**
* Added liveness and readiness probes to Kubernetes manifests.
* Set resource requests and limits for CPU and memory per container.
* Defined securityContext to run containers as non-root users.
* Enabled rolling updates for zero-downtime deployments.

**Proof**:
- `backend-deployment.yaml`:
  - `readinessProbe`, `livenessProbe`
  - `resources:`
  - `securityContext:`

 **Part 6 - Observability with Monitoring and Logging**
* Integrated Prometheus with FastAPI’s /metrics endpoint using starlette_exporter.
* Deployed Grafana, linked to Prometheus as a data source.
* Created dashboards to monitor:
 - API request count and latency.
 - Authentication success/failure rates.
 - Database connection health.
* Logging stack (EFK) proposed for future centralized log collection.

**Proof**:
- `prometheus/prometheus.yml`
- `app/main.py` imports and exposes metrics
- `grafana-deployment.yaml`

![Image](https://github.com/user-attachments/assets/69e64102-dd93-4237-b697-e12382d7b114)


## Summary of Evidence Files

| Milestone                     | Files/Folders                                              |
|------------------------------|------------------------------------------------------------|
| Kubernetes Deployment        | `k8s/*.yaml`, `Dockerfile`                                |
| Config Management            | `secrets.yaml`, `configmap.yaml`, `main.py`               |
| Persistent Storage           | `postgres-pvc.yaml`, `postgres-deployment.yaml`           |
| Ingress Setup                | `ingress.yaml`, `/etc/hosts`                              |
| Probes & Resources           | `backend-deployment.yaml`                                 |
| Monitoring                   | `prometheus.yml`, `main.py`, `grafana-deployment.yaml`    |
| CI/CD + Helm                 | `.github/workflows/`, `helm/`, `values.yaml`              |



## Challenges Faced

**3.1 Application Crashing on Startup**

<pre> ModuleNotFoundError: No module named 'database' </pre>

Root cause: incorrect import path inside Docker container due to mismatched module structure.

**3.2 Prometheus/Grafana Metrics Not Visible**

Prometheus UI was accessible on localhost:9090 but showed no active targets or data.

Grafana dashboards remained empty.

Actions Taken:

  - Confirmed FastAPI /metrics endpoint was reachable.

  - Inspected container logs and Prometheus status.
  
**3.3 Local Port Conflicts (Windows)**

Prometheus port (9090) was occasionally stuck in TIME_WAIT.

Resolution:

- Restarted Prometheus container/service.
   
- Ensured only one service bound to port 9090

## Key Takeaways

Gained hands-on experience managing complex Kubernetes deployments.

Learned the practical utility of volumes, Secrets, and multi-replica services.

Developed a better understanding of how declarative infrastructure supports scaling and resiliency.

## Conclusion

This project provided an excellent platform to reinforce theoretical Kubernetes concepts with practical, scenario-based learning. Each phase added a layer of complexity, mirroring real-world engineering challenges. The experience has improved my ability to design, deploy, and manage Kubernetes-native applications effectively.
