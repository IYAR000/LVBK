# Getting Started with LVBK

This guide will help you set up and start using the LVBK Martial Arts Computer Vision AI System.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### System Requirements

- **Operating System**: Ubuntu 22.04 LTS, Windows 11, or macOS
- **Python**: Version 3.10 or 3.11
- **Memory**: Minimum 8GB RAM (16GB recommended for training)
- **Storage**: At least 10GB free space
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)

### Required Software

- **Git**: For version control
- **Git LFS**: For large file storage
- **Podman**: For containerization (or Docker as alternative)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/IYAR000/LVBK.git
cd LVBK
```

### Step 2: Set Up Git LFS

```bash
# Install Git LFS if not already installed
# Ubuntu/Debian:
sudo apt install git-lfs

# macOS:
brew install git-lfs

# Windows:
# Download from https://git-lfs.github.io/

# Initialize Git LFS
git lfs install
git lfs pull
```

### Step 3: Create Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Step 5: Configure Environment

```bash
# Copy example environment file
cp env.example .env

# Edit the .env file with your configuration
nano .env  # or use your preferred editor
```

Required environment variables:

```bash
# IBM Watson Configuration
IBM_WATSON_API_KEY=your_watson_api_key
IBM_WATSON_PROJECT_ID=your_project_id
IBM_WATSON_URL=https://us-south.ml.cloud.ibm.com

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/lvbk

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

## 🐳 Container Setup (Recommended)

### Using Podman

```bash
# Build the container
podman build -t lvbk .

# Run with Podman Compose
podman-compose up -d

# Check running services
podman-compose ps
```

### Using Docker (Alternative)

```bash
# Build the container
docker build -t lvbk .

# Run with Docker Compose
docker-compose up -d

# Check running services
docker-compose ps
```

## 🔧 Development Setup

### Step 1: Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Step 2: Set Up Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
```

### Step 3: Run Initial Tests

```bash
# Run unit tests
pytest tests/unit/

# Run all tests with coverage
pytest tests/ --cov=src/
```

## 🚀 Quick Start

### Start the API Server

```bash
# Using Python directly
uvicorn src.lvbk.api.main:app --host 0.0.0.0 --port 8000 --reload

# Using Podman Compose
podman-compose up -d

# Using Docker Compose
docker-compose up -d
```

### Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Alternative Docs**: http://localhost:8000/redoc

### Test the Installation

```bash
# Test API health
curl http://localhost:8000/health

# Test with a sample request
curl -X POST "http://localhost:8000/api/analyze" \
     -H "Content-Type: multipart/form-data" \
     -F "video=@sample_video.mp4" \
     -F "martial_art=silat_lincah"
```

## 📊 Using the API

### Python Client Example

```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

# Upload and analyze a video
def analyze_video(video_path: str, martial_art: str):
    url = f"{BASE_URL}/api/analyze"
    
    with open(video_path, 'rb') as f:
        files = {'video': f}
        data = {'martial_art': martial_art}
        
        response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Analysis failed: {response.text}")

# Example usage
try:
    result = analyze_video("technique_video.mp4", "silat_lincah")
    print(f"Technique: {result['technique']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Analysis: {result['analysis']}")
except Exception as e:
    print(f"Error: {e}")
```

### JavaScript Client Example

```javascript
// Upload and analyze a video
async function analyzeVideo(videoFile, martialArt) {
    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('martial_art', martialArt);
    
    try {
        const response = await fetch('http://localhost:8000/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Technique:', result.technique);
            console.log('Confidence:', result.confidence);
            return result;
        } else {
            throw new Error(`Analysis failed: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Example usage
const videoInput = document.getElementById('video-input');
const martialArtSelect = document.getElementById('martial-art-select');

videoInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file) {
        try {
            const result = await analyzeVideo(file, martialArtSelect.value);
            displayResults(result);
        } catch (error) {
            console.error('Analysis failed:', error);
        }
    }
});
```

## 🎯 Supported Martial Arts

### Silat Lincah
- **Description**: Malaysian Martial Art
- **Focus**: Fluid movements and techniques
- **Supported Techniques**: Langkah Tiga, Jurus, Bunga Sembah

### Vovinam Viet Vo Dao
- **Description**: Vietnamese martial art
- **Focus**: Combination of hard and soft techniques
- **Supported Techniques**: Basic forms, Self-defense techniques

### Brazilian Jiu-Jitsu
- **Description**: Ground-based grappling martial art
- **Focus**: Submissions and positional control
- **Supported Techniques**: Guard passes, Submissions, Escapes

### Kyokushin Nakamura
- **Description**: Full-contact karate style
- **Focus**: Powerful strikes and conditioning
- **Supported Techniques**: Kicks, Punches, Kata forms

## 📁 Data Preparation

### Video Requirements

- **Format**: MP4 (H.264), MOV, AVI
- **Maximum Size**: 1GB per file
- **Duration**: 5-60 seconds recommended
- **Resolution**: 720p or higher
- **Frame Rate**: 24-60 FPS

### Annotation Format

The system expects annotations in COCO format:

```json
{
    "images": [
        {
            "id": 1,
            "file_name": "technique_001.jpg",
            "width": 1920,
            "height": 1080
        }
    ],
    "annotations": [
        {
            "id": 1,
            "image_id": 1,
            "category_id": 1,
            "keypoints": [x1, y1, v1, x2, y2, v2, ...],
            "num_keypoints": 17
        }
    ],
    "categories": [
        {
            "id": 1,
            "name": "person",
            "keypoints": ["nose", "left_eye", ...],
            "skeleton": [[16, 14], [14, 12], ...]
        }
    ]
}
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# If you get import errors, ensure the package is installed
pip install -e .
```

#### 2. GPU Not Detected
```bash
# Check CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# Install CUDA-specific PyTorch if needed
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 3. API Connection Issues
```bash
# Check if the API is running
curl http://localhost:8000/health

# Check container logs
podman-compose logs api
```

#### 4. Memory Issues
```bash
# Reduce batch size in config files
# Or increase system memory
# Consider using cloud instances for large datasets
```

### Getting Help

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Wiki**: Detailed documentation and tutorials
- **Email**: Contact maintainers for critical issues

## 📚 Next Steps

1. **Explore the API**: Try different endpoints and features
2. **Read the Documentation**: Check out the full API documentation
3. **Join the Community**: Participate in discussions and contribute
4. **Train Custom Models**: Follow the training guide for your martial art
5. **Deploy to Production**: Use the deployment guide for cloud setup

## 🔗 Additional Resources

- [API Documentation](api/)
- [Architecture Overview](../architecture/)
- [Training Guide](training.md)
- [Deployment Guide](deployment.md)
- [Contributing Guide](../../CONTRIBUTING.md)

---

Welcome to LVBK! We're excited to see what you'll build with our martial arts analysis system. 🥋
