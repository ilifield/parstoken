# Contributing to Parstoken

Thank you for your interest in contributing to Parstoken! This document provides
guidelines and instructions for contributing.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/ilifield/parstoken.git
   cd parstoken
   ```
3. **Install** development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=parstoken --cov-report=term-missing
```

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
ruff check src/ tests/
ruff format src/ tests/
```

### Type Checking

```bash
mypy src/parstoken/
```

## Submitting Changes

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes and add tests

3. Ensure all tests pass:
   ```bash
   pytest
   ```

4. Commit your changes with a clear message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

5. Push to your fork and submit a pull request

## Pull Request Guidelines

- Include tests for any new functionality
- Update documentation if needed
- Follow existing code style and conventions
- Keep changes focused — one feature or fix per PR
- Write clear commit messages

## Reporting Issues

When reporting issues, please include:

- Python version (`python --version`)
- Parstoken version (`parstoken --version`)
- Minimal code example that reproduces the issue
- Expected vs actual behavior

## Adding New Features

If you'd like to add a new feature:

1. Open an issue first to discuss the feature
2. Wait for feedback from maintainers
3. Implement the feature with tests
4. Submit a pull request

## Code of Conduct

Please be respectful and constructive in all interactions. We are committed to
providing a welcoming and inclusive environment for everyone.

## Questions?

Feel free to open an issue for any questions about contributing.
