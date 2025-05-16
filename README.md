# widgetario-k8s

This repository contains the work completed during the Kubernetes CourseLabs Hackathon. In order to replicate a real-world use case, the goal was to deploy and manage a multi-component application in a Kubernetes environment. A To-Do List application had been deployed, applying theoretical understanding of Kubernetes to real-world implementation challenges involving application deployment, configuration, storage, and scaling.

# Objectives

The main goals of the project were:

To design Kubernetes manifests for a multi-tier application.

To implement secure environment configurations using Secrets and ConfigMaps.

To handle both ephemeral and persistent storage needs within the cluster.

To scale services and apply service exposure techniques like load balancing.

# Tools and Technologies Used

Kubernetes

kubectl

Minikube (for local cluster setup)

Docker

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

Managing interdependent services and ensuring startup order.

Debugging misconfigured environment variables and service ports.

Ensuring proper persistence settings during database restarts.

These challenges were addressed through pod inspection, logs analysis, and testing each component in isolation before integration.

# Key Takeaways

Gained hands-on experience managing complex Kubernetes deployments.

Learned the practical utility of volumes, Secrets, and multi-replica services.

Developed a better understanding of how declarative infrastructure supports scaling and resiliency.

# Conclusion

This project provided an excellent platform to reinforce theoretical Kubernetes concepts with practical, scenario-based learning. Each phase added a layer of complexity, mirroring real-world engineering challenges. The experience has improved my ability to design, deploy, and manage Kubernetes-native applications effectively.
