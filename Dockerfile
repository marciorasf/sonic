FROM python:3.10

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-root --no-dev
COPY sonic/ /app/sonic/

# Add dependencies to run the performance tests
RUN pip install py-spy
RUN apt install procps -y

EXPOSE 8000

CMD ["poetry", "run", "opentelemetry-instrument", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "sonic.main:app", "--log-level", "warning"]
