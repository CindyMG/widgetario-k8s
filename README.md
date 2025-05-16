# widgetario-k8s

This repository outlines the progress made on the development and deployment of a containerized
FastAPI-based To-Do application using Kubernetes, Docker, and CI/CD pipelines. The system
integrates observability tools such as Prometheus and Grafana, and follows best practices for modern
DevOps workflows including configuration management, persistent storage, and readiness for production
environments.

# Objectives

The main goals of the project were:

- To design Kubernetes manifests for a multi-tier application.

- To implement secure environment configurations using Secrets and ConfigMaps.

- To handle both ephemeral and persistent storage needs within the cluster.

- To scale services and apply service exposure techniques like load balancing.

# Tools and Technologies Used

Kubernetes

kubectl

Minikube (for local cluster setup)

Docker

# Cloning the Repository

1. Have a running Kubernetes cluster (e.g., Minikube).
2. Clone the repository:

```bash
git clone https://github.com/CindyMG/widgetario-k8s
```
3. Navigate to the directory
```bash
cd 
```

# Project Breakdown

**Part 1: Application Deployment**

**Part 2: Configuration**

 **Part 3: Storage**

 **Part 4 - Ingress**

 **Part 5 - Productionizing**

 **Part 6 - Observability**

 **Part 7 - CI/CD**

**Cleanup** 

# Challenges Faced

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

# Key Takeaways

Gained hands-on experience managing complex Kubernetes deployments.

Learned the practical utility of volumes, Secrets, and multi-replica services.

Developed a better understanding of how declarative infrastructure supports scaling and resiliency.

# Conclusion

This project provided an excellent platform to reinforce theoretical Kubernetes concepts with practical, scenario-based learning. Each phase added a layer of complexity, mirroring real-world engineering challenges. The experience has improved my ability to design, deploy, and manage Kubernetes-native applications effectively.
