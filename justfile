dev-server:
	poetry run opentelemetry-instrument uvicorn sonic.api.main:app --reload
