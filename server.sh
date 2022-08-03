#!/bin/bash

poetry run opentelemetry-instrument uvicorn sonic.main:app --reload
