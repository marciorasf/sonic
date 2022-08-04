#!/bin/bash

poetry run opentelemetry-instrument uvicorn sonic.entrypoints.fastapi_app:app --reload
