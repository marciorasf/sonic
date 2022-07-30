# Performance Tests

## Requirements

- Install Node.js and yarn
- Install Docker and DockerCompose

## Run tests

1. Go to the performance folder:

   ```bash
   cd tests/performance
   ```

2. Install dependencies:

   ```bash
   yarn install
   ```

3. Start Prometheus, Grafana and Sonic:

   ```bash
   docker-compose up --build
   ```

4. Run the test (change to the test you want):

   ```bash
   # The test's name must be the same as the filename (without extension).
   ./run_test test_example
   ```

5. The progress will be displayed while the test is running.

6. After it finishes, the result summary will be displayed on the terminal. You can also find the test's logs and summary and profile in `reports/`. If you want to check the metrics during the test, see [Grafana](http://localhost:3000) or [Prometheus](http://localhost:9090).
