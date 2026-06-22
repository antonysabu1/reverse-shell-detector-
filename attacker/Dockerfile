FROM ubuntu:22.04

# Prevent interactive timezone prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary networking tools
RUN apt-get update && apt-get install -y \
    netcat \
    socat \
    python3 \
    iproute2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/attacker

# By default, keep the container running
CMD ["tail", "-f", "/dev/null"]
