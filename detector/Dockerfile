FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tcpdump \
    iproute2 \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/detector

# Install Python dependencies for packet capture/analysis
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# By default, keep the container running
CMD ["tail", "-f", "/dev/null"]
