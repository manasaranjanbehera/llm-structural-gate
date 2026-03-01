format:
	ruff format .

lint:
	ruff check .

# Applies safe Ruff auto-fixes only. Does not use --unsafe-fixes.
# Prefer ruff check . (no fix) in CI to avoid unintended changes.
fix:
	ruff check . --fix
