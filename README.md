# CI/CD for a Microservice Application 🚀
## food-order-system-microservice-application-v1

This repository contains a **hands-on DevOps project** that demonstrates how to design, automate, secure, and deploy a **microservice-based application** using modern **CI/CD pipelines** and **Kubernetes** best practices.

The project is built as a **production-like, lab setup** to gain real-world experience with DevOps tools, workflows, and cloud-native deployment patterns.

---

## 🧱 Architecture Overview

The application follows a **microservices architecture** and consists of:

* **Admin UI**
* **Admin Backend Service**
* **Customer UI**
* **Customer Backend Service**
* **Notification Service**
* **PostgreSQL Database** (StatefulSet)

All services are containerized and deployed to a **K3s Kubernetes cluster** using **Helm charts**.

> ⚠️ Note: This is a learning-focused, self-hosted Kubernetes environment designed to closely resemble real-world production workflows.

---

## ⚙️ CI/CD Architecture

CI and CD pipelines are implemented as **separate Jenkins pipelines** to improve reliability and follow DevOps best practices.

### 🔁 CI Pipeline (Continuous Integration)

Triggered on code changes pushed to GitHub.

**Steps:**

1. Source code checkout from GitHub
2. Code quality analysis using **SonarQube**
3. Vulnerability scanning using **Trivy** (filesystem)
4. Docker image build
5. Container image vulnerability scanning using **Trivy**
6. Image tagging and push to **Nexus Repository**
7. Email notification on pipeline status

---

### 🚀 CD Pipeline (Continuous Deployment)

Triggered after a successful CI pipeline or manually.

**Steps:**

1. Fetch Helm charts
2. Deploy / upgrade application using **Helm**
3. Automated rollout to **K3s Kubernetes cluster**
4. Email notification on deployment status

---

## 🔐 Security Practices Implemented

* Static code analysis with **SonarQube**
* Vulnerability scanning of source code and container images using **Trivy**
* Non-root containers where applicable
* Secrets and configuration managed via Kubernetes best practices
* HTTPS (TLS) enabled for ingress traffic

---

## 🧰 Tools & Technologies

| Category            | Tools            |
| ------------------- | ---------------- |
| CI/CD               | Jenkins          |
| Containerization    | Docker           |
| Orchestration       | Kubernetes (K3s) |
| Package Management  | Helm             |
| Code Quality        | SonarQube        |
| Security Scanning   | Trivy            |
| Artifact Repository | Nexus Repository |
| SCM                 | GitHub           |
| Database            | PostgreSQL       |

---

## 📁 Repository Structure

```bash
.
├── admin-ui/
├── admin-backend/
├── customer-ui/
├── customer-backend/
├── notification-service/
├── helm-charts/
│   ├── admin-ui/
│   ├── admin-backend/
│   ├── customer-ui/
│   ├── customer-backend/
│   ├── notification-service/
│   └── postgres/
├── k8s-manifests/
├── jenkins/
│   ├── ci-pipeline.groovy
│   └── cd-pipeline.groovy
└── README.md
```

---

## ▶️ How to Deploy (High Level)

1. Provision a K3s cluster
2. Install Jenkins, SonarQube, Nexus, and Trivy
3. Configure Jenkins credentials and tools
4. Run CI pipeline to build and push images
5. Run CD pipeline to deploy the application using Helm
6. Access the application via configured domain and HTTPS

---

## 🎯 Learning Outcomes

Through this project, I gained hands-on experience with:

* Designing CI/CD pipelines for microservices
* Kubernetes deployments and StatefulSets
* Helm-based application delivery
* Container security and vulnerability management
* Operating a production-like Kubernetes environment

---

## 📌 Future Improvements

* Multi-node Kubernetes cluster
* GitOps-based CD using Argo CD or Flux
* Centralized logging (ELK / Loki)
* Monitoring with Prometheus & Grafana
* Automated rollback strategies

---

## 👤 Author

**Gimhan Perera**
DevOps / Cloud Enthusiast

---

⭐ If you find this project useful, feel free to star the repository!
