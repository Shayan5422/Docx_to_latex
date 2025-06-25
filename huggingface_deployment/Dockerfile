FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy core application files
COPY app.py .
COPY web_api.py .
COPY converter.py .
COPY preserve_linebreaks.lua .

# Create necessary directories
RUN mkdir -p temp/uploads temp/outputs

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=7860

# Run the application
CMD ["python", "app.py"] 