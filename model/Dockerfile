FROM python:3.10-slim

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY serve.py .

# Expose port for FastAPI
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
