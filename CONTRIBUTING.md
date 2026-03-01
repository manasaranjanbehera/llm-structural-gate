# Contributing to Structural Gate

Thank you for your interest in contributing. This document covers local setup, tests, and how to submit issues and pull requests.

## Introduction

This project is a pure strict structural enforcement prototype. We welcome contributions that improve documentation, tests, or tooling. Changes to core application logic should be discussed first (e.g. via an issue).

## Local setup

1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the API locally (optional):

   ```bash
   uvicorn app.main:app --reload
   ```

   Server: `http://127.0.0.1:8000`

## How to run tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Tests live in `tests/` and cover structural validation behavior (valid passes; enum violation, extra field, missing field, numeric bound, malformed JSON, type/enum violations, and unknown mode return 400 with `status: rejected`).

## Coding guidelines

- Use Python 3.11+.
- Follow existing style in the codebase (4-space indent, no trailing whitespace).
- Keep the scope of this repo to structural validation only; avoid adding semantic checks, retries, or new dependencies unless agreed.
- New behavior should be covered by tests.

## How to submit issues

- **Bugs:** Use the [Bug report](.github/ISSUE_TEMPLATE/bug_report.md) template. Include steps to reproduce, expected vs actual behavior, and environment details.
- **Features:** Use the [Feature request](.github/ISSUE_TEMPLATE/feature_request.md) template. Describe the problem and proposed solution.
- **Security:** Do **not** open a public issue for security vulnerabilities. See [SECURITY.md](SECURITY.md).

## How to submit pull requests

1. Open an issue first if the change is non-trivial, so we can align on approach.
2. Fork the repo, create a branch from `main`, and make your changes.
3. Ensure tests pass: `pytest tests/ -v`.
4. Submit a PR with a clear title and description, referencing any related issue.
5. Address review feedback. Once approved, a maintainer will merge.

We keep process lightweight—no corporate bureaucracy.
