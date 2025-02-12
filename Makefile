.PHONY: venv install serve test lint format clean

# Define variables
PYTHON = python3
VENV = .venv
ACTIVATE = source $(VENV)/bin/activate
APP_MODULE = app.main:app  # Change this based on your project structure
HOST = 0.0.0.0
PORT = 8000
check_dirs := tests app notebooks

# Create a virtual environment using uv
venv:
	uv venv

update:
	uv pip compile pyproject.toml --extra dev > requirements.txt

# Install dependencies from pyproject.toml
install: venv update
	$(ACTIVATE) && uv pip install -r requirements.txt

# Run Uvicorn server
serve:
	$(ACTIVATE) && uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

# Run tests
test:
	$(ACTIVATE) && pytest tests/

# Lint the code with Ruff
lint:
	$(ACTIVATE) && ruff check $(check_dirs)

# Format code with Ruff
format:
	$(ACTIVATE) && ruff format $(check_dirs)

# Clean up generated files
clean:
	rm -rf __pycache__ .pytest_cache $(VENV)

# Help menu
help:
	@echo "Available commands:"
	@echo "  make venv     - Create a virtual environment using uv"  
	@echo "  make update   - capture the dependecies in requirements.txt"
	@echo "  make install  - Install dependencies from pyproject.toml using uv"
	@echo "  make serve    - Start the Uvicorn server"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Lint the code with Ruff"
	@echo "  make format   - Format code with Ruff"
	@echo "  make clean    - Clean up files"
