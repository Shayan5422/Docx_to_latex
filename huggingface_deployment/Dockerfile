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

# Create a user for the application (better security)
RUN useradd -m -u 1000 appuser

# Create necessary directories with proper permissions
RUN mkdir -p /tmp/docx_converter && \
    chmod 777 /tmp/docx_converter && \
    chown -R appuser:appuser /app /tmp/docx_converter

# Switch to the application user
USER appuser

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=7860
ENV TMPDIR=/tmp/docx_converter

# Run the application
CMD ["python", "app.py"] 