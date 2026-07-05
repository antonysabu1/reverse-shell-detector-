FROM ubuntu:22.04

# Prevent interactive timezone prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install tools that might be exploited / used for reverse shells
RUN apt-get update && apt-get install -y \
    netcat \
    python3 \
    php-cli \
    socat \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Install additional tools for Phase 3
RUN apt-get update && apt-get install -y dnsutils && rm -rf /var/lib/apt/lists/*
COPY scripts/ /opt/victim/scripts/
RUN chmod +x /opt/victim/scripts/*.sh

WORKDIR /opt/victim

# By default, keep the container running
CMD ["tail", "-f", "/dev/null"]
