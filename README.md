# LogicLens Detector Service

A Python-based microservice for code plagiarism detection and similarity analysis. This service integrates with the [LogicLens](https://github.com/GabTamayo/LogicLens) platform to provide automated code similarity checking for programming assignments.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Docker Deployment](#-docker-deployment)
- [Integration with LogicLens](#-integration-with-logiclens)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🔍 Overview

The Detector Service is a standalone microservice that analyzes code submissions for potential plagiarism and similarity. It uses advanced algorithms to compare code structures, variable names, and patterns to identify similarities between student submissions.

### Key Capabilities

- **Code Similarity Detection**: Compare two or more code submissions
- **Plagiarism Analysis**: Identify potential academic dishonesty
- **Multi-Language Support**: Works with various programming languages
- **Asynchronous Processing**: Handle multiple detection requests concurrently
- **RESTful API**: Easy integration with any platform

## ✨ Features

- **Fast Detection**: Optimized algorithms for quick similarity analysis
- **Detailed Reports**: Comprehensive similarity metrics and matching segments
- **Scalable Architecture**: Handle multiple concurrent requests
- **Docker Support**: Easy deployment with containerization
- **API Documentation**: Auto-generated interactive API docs
- **CORS Enabled**: Ready for cross-origin requests
- **Health Checks**: Built-in endpoints for monitoring

## 🛠 Tech Stack

- **Python 3.9+** - Core programming language
- **FastAPI** - Modern web framework for APIs
- **Uvicorn** - ASGI server for production
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

### Python Libraries

- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **difflib** / **ast** - Code analysis
- **Additional libraries** - See `requirements.txt`

## 📦 Prerequisites

Choose one of the following setups:

### Option 1: Docker (Recommended)

- Docker Desktop
- Docker Compose

### Option 2: Local Development

- Python 3.9 or higher
- pip (Python package manager)

## 🚀 Installation

### Method 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/GabTamayo/LogicLens-Detector-Service.git
cd LogicLens-Detector-Service

# Build and start the service
docker-compose up -d --build
```

The service will be available at `http://localhost:8001`

### Method 2: Using Docker Manually

```bash
# Clone the repository
git clone https://github.com/GabTamayo/LogicLens-Detector-Service.git
cd LogicLens-Detector-Service

# Build the Docker image
docker build -t logiclens-detector .

# Run the container
docker run -d -p 8001:8001 --name detector logiclens-detector
```

### Method 3: Local Development Setup

```bash
# Clone the repository
git clone https://github.com/GabTamayo/LogicLens-Detector-Service.git
cd LogicLens-Detector-Service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The service will be available at `http://localhost:8001`

## 📡 API Endpoints

### Health Check

```http
GET /
```

Returns service status and version information.

**Response:**

```json
{
  "status": "healthy",
  "service": "LogicLens Detector Service",
  "version": "1.0.0"
}
```

### Detect Code Similarity

```http
POST /detect
```

Analyzes code submissions for similarity.

**Request Body:**

```json
{
  "submissions": [
    {
      "id": "student_1",
      "code": "def hello():\n    print('Hello World')"
    },
    {
      "id": "student_2",
      "code": "def hello():\n    print('Hello World')"
    }
  ],
  "language": "python",
  "threshold": 0.7
}
```

**Response:**

```json
{
  "results": [
    {
      "pair": ["student_1", "student_2"],
      "similarity": 0.95,
      "is_plagiarism": true,
      "details": {
        "matching_lines": 2,
        "total_lines": 2,
        "structural_similarity": 0.98,
        "identifier_similarity": 1.0
      }
    }
  ],
  "summary": {
    "total_comparisons": 1,
    "flagged_submissions": 2,
    "average_similarity": 0.95
  }
}
```

### API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
# Server Configuration
HOST=0.0.0.0
PORT=8001
RELOAD=false

# Detection Settings
DEFAULT_THRESHOLD=0.7
MAX_FILE_SIZE=1048576  # 1MB in bytes

# CORS Settings
ALLOWED_ORIGINS=http://localhost,http://localhost:80
```

### Docker Compose Configuration

Edit `docker-compose.yml` to customize settings:

```yaml
services:
  detector:
    build: .
    ports:
      - "8001:8001"
    environment:
      - HOST=0.0.0.0
      - PORT=8001
    restart: unless-stopped
```

## 💻 Usage

### Example: Python Client

```python
import requests

# Service URL
url = "http://localhost:8001/detect"

# Prepare submissions
payload = {
    "submissions": [
        {
            "id": "submission_1",
            "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
        },
        {
            "id": "submission_2",
            "code": "def fib(num):\n    if num <= 1:\n        return num\n    return fib(num-1) + fib(num-2)"
        }
    ],
    "language": "python",
    "threshold": 0.8
}

# Send request
response = requests.post(url, json=payload)
result = response.json()

print(f"Similarity: {result['results'][0]['similarity']}")
print(f"Plagiarism detected: {result['results'][0]['is_plagiarism']}")
```

### Example: cURL

```bash
curl -X POST http://localhost:8001/detect \
  -H "Content-Type: application/json" \
  -d '{
    "submissions": [
      {
        "id": "sub1",
        "code": "print(\"Hello World\")"
      },
      {
        "id": "sub2",
        "code": "print(\"Hello World\")"
      }
    ],
    "language": "python",
    "threshold": 0.7
  }'
```

### Example: JavaScript/Fetch

```javascript
const detectPlagiarism = async (submissions) => {
  const response = await fetch("http://localhost:8001/detect", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      submissions: submissions,
      language: "python",
      threshold: 0.7,
    }),
  });

  return await response.json();
};
```

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t logiclens-detector:latest .
```

### Run Container

```bash
docker run -d \
  --name detector \
  -p 8001:8001 \
  --restart unless-stopped \
  logiclens-detector:latest
```

### Docker Compose Commands

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Check status
docker-compose ps
```

### Production Deployment

For production, consider:

1. **Use environment variables** for configuration
2. **Enable HTTPS** with reverse proxy (Nginx/Caddy)
3. **Set resource limits** in docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: "1.0"
         memory: 512M
   ```
4. **Configure logging** with proper log drivers
5. **Set up monitoring** with health checks

## 🔗 Integration with LogicLens

The Detector Service is designed to work seamlessly with the main LogicLens application.

### LogicLens Configuration

In your LogicLens `.env` file:

```env
DETECTOR_SERVICE_URL=http://host.docker.internal:8001
```

### Laravel Integration Example

```php
use Illuminate\Support\Facades\Http;

class DetectionService
{
    public function detectPlagiarism(array $submissions)
    {
        $response = Http::post(config('services.detector.url') . '/detect', [
            'submissions' => $submissions,
            'language' => 'python',
            'threshold' => 0.7
        ]);

        return $response->json();
    }
}
```

## 🧪 Development

### Project Structure

```
LogicLens-Detector-Service/
├── api.py                 # API route definitions
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .dockerignore         # Docker ignore patterns
└── README.md             # This file
```

### Running in Development Mode

```bash
# With auto-reload
python main.py --reload

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Adding New Detection Algorithms

1. Create a new detector module in your codebase
2. Implement the detection logic
3. Register the detector in `api.py`
4. Update the API documentation
5. Add tests for the new algorithm

### Testing

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# With coverage
pytest --cov=. --cov-report=html
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Add tests for new features
- Update documentation as needed

## 🔒 Security Considerations

- Implement rate limiting for production deployments
- Validate and sanitize all input code
- Set maximum file size limits
- Use HTTPS in production
- Implement authentication for sensitive endpoints
- Regular security updates for dependencies

## 📊 Performance Optimization

- Use caching for repeated comparisons
- Implement batch processing for multiple submissions
- Consider async processing for large datasets
- Monitor resource usage and optimize as needed

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check if port 8001 is already in use
lsof -i :8001  # On macOS/Linux
netstat -ano | findstr :8001  # On Windows

# Check Docker logs
docker logs detector
docker-compose logs
```

### Connection Refused from LogicLens

If LogicLens can't connect to the detector service:

1. Ensure detector service is running: `docker-compose ps`
2. Check firewall settings
3. Verify `DETECTOR_SERVICE_URL` in LogicLens `.env`
4. Use `host.docker.internal` instead of `localhost` when running in Docker

### High Memory Usage

```bash
# Check resource usage
docker stats detector

# Limit resources in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 512M
```

## 📝 License

This project is part of the LogicLens educational platform and is open-sourced under the [MIT license](LICENSE).

## 👥 Authors

- **Gabriel Tamayo** - _Initial work_ - [@GabTamayo](https://github.com/GabTamayo)

## 🙏 Acknowledgments

- Part of the LogicLens programming assessment platform
- Built for educational purposes
- Designed to promote academic integrity

## 📞 Support

For issues related to the Detector Service:

- Open an issue on [GitHub](https://github.com/GabTamayo/LogicLens-Detector-Service/issues)
- For LogicLens integration issues, see the [main repository](https://github.com/GabTamayo/LogicLens)

---

**Live Demo**: [project-detector-test-service.vercel.app](https://project-detector-test-service.vercel.app)

Made with ❤️ for academic integrity in programming education
