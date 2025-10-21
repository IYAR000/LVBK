# Codecov Setup Guide

This document explains how to set up Codecov integration for the LVBK project's GitHub Actions workflow.

## Prerequisites

- GitHub repository with Actions enabled
- Codecov account (free tier available)

## Setup Steps

### 1. Create Codecov Account

1. Go to [https://codecov.io/](https://codecov.io/)
2. Sign up using your GitHub account
3. Authorize Codecov to access your repositories

### 2. Add Repository to Codecov

1. After signing in, click "Add new repository"
2. Select your LVBK repository from the list
3. Copy the repository token (you'll need this for the next step)

### 3. Add Codecov Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `CODECOV_TOKEN`
5. Value: Paste the token you copied from Codecov
6. Click **Add secret**

### 4. Verify Integration

1. Push a commit to trigger the GitHub Actions workflow
2. Check the Actions tab to ensure the workflow runs successfully
3. Visit your Codecov dashboard to see coverage reports

## Workflow Integration

The workflow is already configured to use Codecov v4 with the following settings:

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    flags: unittests
    name: codecov-umbrella
    token: ${{ secrets.CODECOV_TOKEN }}
```

## Coverage Configuration

Coverage settings are configured in `pyproject.toml`:

- Minimum coverage threshold: 70%
- Coverage reports: XML, HTML, and terminal
- Source directory: `src/lvbk`

## Troubleshooting

### Common Issues

1. **"Codecov token not found"**: Ensure the `CODECOV_TOKEN` secret is properly set
2. **"No coverage data found"**: Check that tests are generating `coverage.xml`
3. **"Upload failed"**: Verify network connectivity and token validity

### Getting Help

- Codecov Documentation: [https://docs.codecov.com/](https://docs.codecov.com/)
- GitHub Actions Documentation: [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

## Optional: Coverage Badge

Add a coverage badge to your README.md:

```markdown
[![codecov](https://codecov.io/gh/yourusername/LVBK/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/LVBK)
```

Replace `yourusername` with your actual GitHub username.




