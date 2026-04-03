# 🚀 DevOps Todo App — Production Pipeline on AWS

![CI/CD](https://github.com/cloudops-mahesh/devops-todo-app/actions/workflows/ci-cd.yml/badge.svg)

A production-ready full-stack Todo application demonstrating 
a complete DevOps pipeline — from code to deployment with 
monitoring on AWS.

> **Live App:** http://YOUR_EC2_IP:3000
> **API Docs:** http://YOUR_EC2_IP:8000/docs

---

## 🏗️ Architecture
```
Developer → GitHub → GitHub Actions CI/CD
                          ↓
                    Run Tests (pytest)
                          ↓
                    Build Docker Images
                          ↓
                    Push to AWS ECR
                          ↓
                    Deploy to AWS EC2
                          ↓
                    App Live on Internet 🌍
                          ↓
                    Prometheus + Grafana
                    (Live Monitoring 📊)
```

---

## 🛠️ Tech Stack

### Application
| Layer | Technology |
|---|---|
| Frontend | React.js |
| Backend | Python FastAPI |
| Database | MongoDB |

### DevOps
| Tool | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| GitHub Actions | CI/CD Pipeline |
| AWS EC2 | Production server |
| AWS ECR | Docker image registry |
| AWS IAM | Security & access management |
| Prometheus | Metrics collection |
| Grafana Cloud | Monitoring dashboards |

---

## 📁 Project Structure
```
devops-todo-app/
├── backend/                 # Python FastAPI
│   ├── main.py              # API endpoints
│   ├── requirements.txt     # Dependencies
│   ├── test_main.py         # Unit tests
│   └── Dockerfile           # Container config
├── frontend/                # React app
│   ├── src/
│   │   └── App.js           # Main component
│   └── Dockerfile           # Multi-stage build
├── nginx/
│   └── nginx.conf           # Reverse proxy config
├── prometheus.yml           # Metrics config
├── docker-compose.yml       # Local development
├── docker-compose.prod.yml  # Production config
└── .github/
    └── workflows/
        └── ci-cd.yml        # GitHub Actions pipeline
```

---

## ⚙️ CI/CD Pipeline

Every `git push` to `main` branch automatically:
```
1. ✅ Runs pytest unit tests
2. 🐳 Builds Docker images
3. 📦 Pushes to AWS ECR
4. 🚀 Deploys to AWS EC2
5. 🔄 Zero downtime restart
```

### Pipeline Stages
```
┌─────────────┐    ┌──────────────────┐    ┌─────────────┐
│  Run Tests  │───▶│ Build & Push ECR │───▶│ Deploy EC2  │
│   ~12s      │    │     ~1m 52s      │    │    ~25s     │
└─────────────┘    └──────────────────┘    └─────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
```
- Docker Desktop installed
- AWS Account
- GitHub Account
```

### Run Locally

**Step 1 — Clone the repo:**
```bash
git clone https://github.com/cloudops-mahesh/devops-todo-app.git
cd devops-todo-app
```

**Step 2 — Start all services:**
```bash
docker-compose up --build
```

**Step 3 — Open in browser:**
```
Frontend: http://localhost:3000
Backend:  http://localhost:8000/docs
```

---

## ☁️ AWS Deployment

### Prerequisites
```bash
# Configure AWS CLI
aws configure

# Set these GitHub Secrets:
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
ECR_REGISTRY
EC2_HOST
EC2_USERNAME
EC2_SSH_KEY
```

### Deploy

Simply push to main branch:
```bash
git add .
git commit -m "your message"
git push origin main
```

GitHub Actions handles everything automatically! ✅

---

## 📊 Monitoring

### Prometheus
```
Metrics endpoint: http://65.0.74.106/metrics
Prometheus UI:    http://65.0.74.106:9090
```

### Grafana Dashboard
Tracks in real time:
- API request rate
- Response times
- Memory usage
- CPU usage
- Error rates

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/todos` | Get all todos |
| POST | `/api/todos` | Create todo |
| PATCH | `/api/todos/{id}` | Toggle complete |
| DELETE | `/api/todos/{id}` | Delete todo |

### Example Request
```bash
# Create a todo
curl -X POST http://YOUR_EC2_IP:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "Learn DevOps!"}'

# Response
{
  "id": "64abc123",
  "task": "Learn DevOps!",
  "completed": false,
  "createdAt": "1234567890"
}
```

---

## 🔒 Security
```
✅ IAM user with least privilege
✅ Secrets stored in GitHub Secrets
✅ Never committed to code
✅ Security groups (firewall rules)
✅ SSH key authentication
```

---

## 🧪 Testing
```bash
# Run tests locally
cd backend
python -m pytest test_main.py -v

# Test results:
✅ test_health_check
✅ test_metrics_endpoint  
✅ test_api_todos_endpoint_exists
```

---

## 📈 What I Learned
```
✅ Docker multi-stage builds
✅ AWS IAM, EC2, ECR
✅ GitHub Actions CI/CD
✅ Prometheus metrics
✅ Grafana dashboards
✅ Linux server management
✅ Production deployment practices
```

---

## 🔜 Future Improvements
```
⬜ Add Kubernetes (EKS)
⬜ Add Terraform (IaC)
⬜ Add SonarQube (code quality)
⬜ Add Trivy (security scanning)
⬜ Add ArgoCD (GitOps)
⬜ Add HTTPS with SSL certificate
```

---

## 👨‍💻 Author

**Mahesh** — DevOps Engineer

[![LinkedIn]](www.linkedin.com/in/mahesh-panchal-4683501a1)
[![GitHub]](https://github.com/cloudops-mahesh)

---

## ⭐ If you found this useful, please star the repo!