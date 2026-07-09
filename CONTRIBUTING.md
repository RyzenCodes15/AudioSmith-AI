# Contributing to AudioSmith AI

First off, thank you for considering contributing to AudioSmith AI! It's people like you that make this tool great.

## Development Setup

The project uses Docker Compose to orchestrate the full stack locally.

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/AudioSmith.git
cd AudioSmith

# 2. Setup environment variables
cp .env.example .env
# Edit .env with your local settings if necessary

# 3. Start the stack
make dev
```

## Development Workflow

We use a feature-branch workflow.

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make your changes.
3. Run tests and linters:
   ```bash
   make test
   make lint
   ```
4. Commit your changes following Conventional Commits.
5. Push to your fork and submit a Pull Request.

## Code Style

### Python (Backend & ML)
- Formatter: `ruff format`
- Linter: `ruff check`
- Type checking: `mypy` (strict mode)
- Docstrings: Google style

### TypeScript (Frontend)
- Formatter: Prettier
- Linter: ESLint
- Type checking: TypeScript (`strict: true`)

## Submitting Pull Requests

Please ensure your PR description clearly describes the problem and solution. Include any relevant issue numbers. Your PR must pass all CI checks before it can be merged.
