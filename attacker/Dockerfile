FROM ubuntu:22.04

# Prevent interactive timezone prompts
ENV DEBIAN_FRONTEND=noninteractive


# Install necessary networking tools
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    socat \
    python3 \
    iproute2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/attacker

# Install additional tools for Phase 3
RUN apt-get update && apt-get install -y dnsmasq python3-pip && pip3 install --no-cache-dir dnslib && rm -rf /var/lib/apt/lists/*
COPY scripts/ /opt/attacker/scripts/
RUN chmod +x /opt/attacker/scripts/*.sh
CMD ["tail","-f","/dev/null"]
