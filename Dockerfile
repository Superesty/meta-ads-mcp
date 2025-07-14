FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
RUN pip install --upgrade pip && \
    pip install uv

# Copy requirements file
COPY requirements.txt .

# Install dependencies using uv with --system flag
RUN uv pip install --system -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the package in development mode
RUN uv pip install --system -e .

# Expose port 8080 for HTTP transport
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH="/app"
ENV MCP_LOG_LEVEL="INFO"

# Command to run the Meta Ads MCP server in HTTP mode
CMD ["python", "-m", "meta_ads_mcp", "--transport", "streamable-http", "--port", "8080", "--host", "0.0.0.0"] 