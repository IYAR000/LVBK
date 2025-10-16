# LVBK Setup Documentation

This directory contains setup guides for various components and integrations of the LVBK project.

## Available Guides

- [Codecov Setup](codecov_setup.md) - Instructions for setting up code coverage reporting with Codecov

## GitHub Actions

The project uses GitHub Actions for CI/CD with the following features:

- **Testing**: Unit and integration tests with Python 3.10 and 3.11
- **Code Quality**: Linting with flake8, formatting with black, type checking with mypy
- **Security**: Vulnerability scanning with safety and bandit
- **Containerization**: Podman-based container builds
- **Coverage**: Code coverage reporting with Codecov

## Quick Start

1. Set up Codecov integration (see [Codecov Setup](codecov_setup.md))
2. Push changes to trigger the workflow
3. Monitor the Actions tab for build status
4. Check Codecov dashboard for coverage reports

## Requirements

- GitHub repository with Actions enabled
- Codecov account (for coverage reporting)
- Podman (for container builds)

## Troubleshooting

For issues with specific components, refer to the individual setup guides in this directory.
