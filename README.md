# Budget Tracker

A Flask-based budget tracking application with CI/CD pipeline and monitoring.

## Live Demo
🌐 **Deployed at**: https://budget-tracker-ia.onrender.com

## Features
- Track income and expenses
- Categorize transactions
- Export to CSV
- RESTful API
- Prometheus metrics

## Run Locally
```bash
pip install -r requirements.txt
flask run
```

## Run Tests
```bash
pytest tests/ --cov=app --cov-report=term
```

## Docker
```bash
docker build -t budget-tracker .
docker run -p 5000:5000 budget-tracker
```

## Docker Compose (with Prometheus)
```bash
docker-compose up --build
```
- App: http://localhost:5000
- Health: http://localhost:5000/health
- Metrics: http://localhost:5000/metrics
- Prometheus: http://localhost:9090

## CI/CD Pipeline
GitHub Actions runs:
1. **Lint** - Code quality with flake8
2. **Test** - Unit tests with 70% coverage requirement
3. **Build** - Docker image build + health check
4. **Deploy** - Auto-deploy to Render (main branch only)

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard |
| `/health` | GET | Health check |
| `/api/summary` | GET | Monthly summary JSON |
| `/transactions` | GET | List transactions |
| `/transactions/new` | GET/POST | Create transaction |
| `/categories` | GET | List categories |
| `/export.csv` | GET | Export CSV |