# Contributing to LVBK

Thank you for your interest in contributing to the LVBK Martial Arts Computer Vision AI System! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - System information (OS, Python version)
   - Steps to reproduce
   - Expected vs actual behavior
   - Logs and error messages

### Suggesting Enhancements

We welcome suggestions for new features and improvements:

1. **Check existing discussions** first
2. **Use the enhancement template** for feature requests
3. **Provide clear use cases** and rationale
4. **Consider implementation complexity**

### Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/LVBK.git
   cd LVBK
   ```
3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

#### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Run tests and checks**:
   ```bash
   pytest tests/
   black --check src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

## 📋 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line length**: 88 characters (Black default)
- **Import order**: Standard library, third-party, local imports
- **Type hints**: Required for all function signatures
- **Docstrings**: Google style for all public functions/classes

### Code Formatting

We use **Black** for automatic code formatting:

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting

We use **Flake8** for code linting:

```bash
# Run linting
flake8 src/ tests/
```

### Type Checking

We use **MyPy** for static type checking:

```bash
# Type check
mypy src/
```

### Example Code Style

```python
from typing import List, Dict, Optional
import numpy as np

def analyze_technique(
    pose_sequence: np.ndarray,
    martial_art: str,
    confidence_threshold: float = 0.7
) -> Dict[str, any]:
    """
    Analyze martial arts technique from pose sequence.
    
    Args:
        pose_sequence: Array of pose keypoints (frames, keypoints, coords)
        martial_art: Name of martial art discipline
        confidence_threshold: Minimum confidence for classification
        
    Returns:
        Dictionary containing technique classification results
        
    Raises:
        ValueError: If martial_art is not supported
        
    Example:
        >>> poses = np.random.rand(30, 17, 2)
        >>> result = analyze_technique(poses, "Silat Lincah")
        >>> print(result['technique'])
        'Langkah Tiga'
    """
    if martial_art not in SUPPORTED_MARTIAL_ARTS:
        raise ValueError(f"Unsupported martial art: {martial_art}")
    
    # Implementation here
    pass
```

## 🧪 Testing

### Writing Tests

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test component interactions
- **Coverage**: Aim for >70% code coverage

### Test Structure

```python
# tests/unit/test_technique_analysis.py
import pytest
import numpy as np
from lvbk.models.technique_analyzer import TechniqueAnalyzer

class TestTechniqueAnalyzer:
    def test_analyze_technique_success(self):
        """Test successful technique analysis."""
        analyzer = TechniqueAnalyzer()
        poses = np.random.rand(30, 17, 2)
        
        result = analyzer.analyze(poses, "silat_lincah")
        
        assert result['technique'] is not None
        assert result['confidence'] > 0.0
        
    def test_analyze_technique_invalid_martial_art(self):
        """Test error handling for invalid martial art."""
        analyzer = TechniqueAnalyzer()
        poses = np.random.rand(30, 17, 2)
        
        with pytest.raises(ValueError):
            analyzer.analyze(poses, "invalid_art")
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/

# Run specific test file
pytest tests/unit/test_technique_analysis.py

# Run with verbose output
pytest tests/ -v
```

## 📝 Documentation

### Code Documentation

- **Module docstrings**: Explain module purpose and usage
- **Class docstrings**: Document attributes and methods
- **Function docstrings**: Use Google style format
- **Inline comments**: Explain complex logic

### API Documentation

- **OpenAPI/Swagger**: Auto-generated from FastAPI code
- **Examples**: Provide usage examples for all endpoints
- **Error codes**: Document all possible error responses

### User Documentation

- **README**: Keep updated with installation and usage
- **User guides**: Step-by-step instructions
- **Architecture docs**: System design and components

## 🔄 Pull Request Process

### Before Submitting

1. **Run all tests** and ensure they pass
2. **Update documentation** if needed
3. **Add tests** for new features
4. **Update changelog** if applicable

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Address feedback** and make requested changes
4. **Approval** from maintainers
5. **Merge** to main branch

## 🏷️ Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

### Examples

```
feat(mmpose): add Silat Lincah pose estimation model

- Implemented custom keypoint configuration
- Fine-tuned on 500 Silat technique samples
- Achieved 87% accuracy on validation set

Closes #42
```

```
fix(api): resolve video upload timeout issue

- Increased timeout for large file uploads
- Added progress indicators
- Improved error handling

Fixes #123
```

## 🛡️ Security

### Security Considerations

- **Never commit secrets** or API keys
- **Use environment variables** for sensitive configuration
- **Validate all inputs** in API endpoints
- **Follow secure coding practices**

### Reporting Security Issues

For security vulnerabilities, please:

1. **Do not create public issues**
2. **Email security concerns** to the maintainers
3. **Provide detailed information** about the vulnerability
4. **Allow time for response** before public disclosure

## 🏆 Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **GitHub contributor statistics**

## 📞 Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Wiki**: For detailed documentation and guides

## 📄 License

By contributing to LVBK, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LVBK! Your efforts help make martial arts analysis more accessible and accurate. 🥋





