pip install -r requirements.txt
Run main.py

## Docker

To run the application using Docker:

1. Build the Docker image:
   ```
   docker build -t capstone-detector .
   ```

2. Run the container:
   ```
   docker run -p 8001:8001 capstone-detector
   ```

Alternatively, using Docker Compose:

1. Build and run:
   ```
   docker-compose up --build
   ```

The API will be available at http://localhost:8001