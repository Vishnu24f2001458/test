# Use Python 3.11 slim image
FROM python:3.11-slim

# Create non-root user with UID 1000
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /home/appuser/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining files
COPY . .

# Set environment variable for app port
ENV APP_PORT=7362

# Change ownership and switch to non-root user
RUN chown -R appuser:appuser /home/appuser
USER appuser

# Expose port
EXPOSE 7362

# Run FastAPI app via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7362"]
