ARG PYTHON_BASE=3.10-slim

# Build stage
FROM python:${PYTHON_BASE} AS builder

# Install PDM
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

# Copy necessary files for dependency resolution
COPY pyproject.toml pdm.lock /project/
WORKDIR /project

# Install dependencies
RUN pdm install --check --prod --no-lock --no-editable

# Runtime stage
FROM python:${PYTHON_BASE}

# Set environment variables
ENV PYTHONPATH=/app
ENV PATH="/project/.venv/bin:${PATH}"

# Copy application code and necessary files
COPY --from=builder /project/.venv /project/.venv

# Copy only required directories and files
COPY main.py /app/
COPY domain /app/domain
COPY infrastructure /app/infrastructure
COPY alembic /app/alembic
COPY alembic.ini /app/

WORKDIR /app

CMD ["sh", "-c", "alembic upgrade head && python main.py"]