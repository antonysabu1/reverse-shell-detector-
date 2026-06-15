<div align="center">

# 🪤 ShellSnare

**A Dockerized cybersecurity lab for simulating, capturing, and detecting reverse shell connections.**

Multi-layered traffic analysis • Real-time dashboard • 6+ shell types • Fully isolated

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-required-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)

</div>

---

## What is ShellSnare?

Reverse shells are the most common post-exploitation technique used by attackers to maintain remote access to compromised systems. Unlike regular connections, reverse shells originate from the *victim* and connect outbound to the attacker — bypassing most firewall rules.

ShellSnare is a controlled, isolated lab environment for studying how reverse shell connections behave on a network, and how to detect them. Everything runs inside Docker — no real systems are touched.

**What you get:**

- 🗡️ **Controlled Simulations** — Launch 6+ reverse shell types in a sandboxed environment
- 🔎 **Multi-Layered Detection** — Heuristic, statistical, and signature-based traffic analysis
- 📊 **Real-Time Dashboard** — Monitor detections, inspect payloads, and visualize attack patterns
- 🧪 **Study Platform** — Compare detection effectiveness, test evasion, build intuition for malicious traffic

---

## Architecture

ShellSnare runs as a 4-container Docker lab on a shared internal network:

```
┌──────────────────────── Docker Network: shellsnare_lab ────────────────────────┐
│                                                                                │
│   ┌──────────────┐         reverse shell          ┌──────────────┐             │
│   │  🗡️ Attacker  │◄────────────────────────────────│  💻 Victim    │          │
│   │  C2 Listener  │         connection              │  Shell Sim   │           │
│   └──────────────┘                                 └──────────────┘            │
│          ▲                                                ▲                    │
│          │              packet capture                    │                    │
│          └──────────────────┐ ┌───────────────────────────┘                    │
│                        ┌────▼─▼─────┐                                          │
│                        │ 🔎 Detector │                                         │
│                        │   Analysis  │                                         │
│                        │   Engine    │                                         │
│                        └─────┬──────┘                                          │
│                              │ alerts & metrics                                │
│                        ┌─────▼──────┐                                          │
│                        │ 📊 Dashboard│──── Port 8080 ────► 👤 Browser          │
│                        │   Web UI    │                                         │
│                        └────────────┘                                          │
└────────────────────────────────────────────────────────────────────────────────┘
```

| Container | Purpose | Stack |
|-----------|---------|-------|
| **Attacker** | Listens for incoming reverse shell connections, acts as C2 | Netcat, Socat, Python |
| **Victim** | Executes controlled reverse shell payloads on demand | Bash, Python, Netcat, PHP |
| **Detector** | Captures all network traffic and runs detection analysis | Python, Scapy, SQLite |
| **Dashboard** | Serves a real-time web interface for monitoring | Flask, Chart.js, WebSocket |

---

## Detection Engine

ShellSnare uses three complementary detection layers to maximize coverage across shell types:

### 🔤 Signature-Based Detection
Pattern matching against known reverse shell payloads:
- `/bin/bash -i >& /dev/tcp/` — Bash TCP reverse shell
- `python -c 'import socket,subprocess'` — Python socket shell
- `nc -e /bin/bash` — Netcat with execute flag
- Base64/hex encoded shell patterns

### 🧩 Heuristic Analysis
Behavioral indicators that flag suspicious activity:
- **Interactive Session Detection** — Small bidirectional packets with human-speed timing
- **Outbound Connection Profiling** — Unexpected connections to non-standard ports
- **Long-Duration Tracking** — Persistent connections typical of C2 channels
- **Shell Prompt Detection** — Regex matching for `$`, `#`, and shell-like prompts in payloads

### 📊 Statistical Analysis
Mathematical anomaly detection for encrypted/obfuscated shells:
- **Packet Size Distribution** — Reverse shells produce distinct small-packet patterns
- **Inter-Arrival Time Analysis** — Human typing cadence vs. machine-speed transfers
- **Payload Entropy** — High entropy signals encryption or encoding
- **Byte Ratio Analysis** — Asymmetric ratios (small commands → large outputs)
- **Beaconing Detection** — Periodic callback patterns from staged shells

---

## Simulated Shell Types

| Type | Detection Difficulty | Description |
|------|---------------------|-------------|
| Bash TCP | 🟢 Easy | Classic `/dev/tcp` based reverse shell |
| Netcat | 🟢 Easy | Traditional `nc -e` reverse shell |
| Python | 🟡 Medium | Socket + subprocess based shell |
| PHP | 🟡 Medium | `fsockopen` based reverse shell |
| Socat Encrypted | 🔴 Hard | SSL/TLS encrypted reverse shell |
| DNS Tunneled | 🔴 Hard | Commands tunneled over DNS queries |

---

## Dashboard

The real-time web dashboard at `http://localhost:8080` provides:

- 🔴 **Live Alert Feed** — Chronological stream of detected reverse shell events
- 🗺️ **Network Flow Map** — Visual representation of connections between containers
- 📈 **Traffic Statistics** — Packet rates, byte ratios, and entropy charts
- 🔍 **Payload Inspector** — Hex/ASCII view of captured suspicious payloads
- 🏷️ **Attack Classification** — Auto-categorization of detected shell types
- 📊 **Confidence Scoring** — Multi-indicator confidence gauge per detection
- ⏪ **Session Replay** — Reconstruct and review captured shell sessions

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) v20.10+
- [Docker Compose](https://docs.docker.com/compose/) v2.0+

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shellsnare.git
cd shellsnare

# Build and start all containers
docker compose up --build
```

Then open **http://localhost:8080** in your browser.

---

## Usage

### 1. Start the lab

```bash
docker compose up --build -d
```

All four containers start automatically. The detector begins capturing traffic immediately.

### 2. Launch a reverse shell

Open a terminal on the victim container:

```bash
docker exec -it shellsnare-victim bash
```

Use the interactive launcher to pick a shell type:

```bash
python3 launcher.py
```

```
╔══════════════════════════════════════╗
║     ShellSnare - Shell Launcher     ║
╠══════════════════════════════════════╣
║  1. Bash TCP Reverse Shell          ║
║  2. Netcat Reverse Shell            ║
║  3. Python Reverse Shell            ║
║  4. PHP Reverse Shell               ║
║  5. Socat Encrypted Shell           ║
║  6. DNS Tunnel Shell                ║
║  0. Exit                            ║
╚══════════════════════════════════════╝
Select shell type:
```

### 3. Watch the dashboard

Open **http://localhost:8080** to see detections appear in real time as you run shells.

### 4. Stop the lab

```bash
docker compose down
```

---

## Project Structure

```
shellsnare/
├── docker-compose.yml            # Orchestrates all 4 containers
│
├── attacker/
│   ├── Dockerfile
│   ├── listener.sh               # Netcat/socat listener scripts
│   └── c2_server.py              # Simple C2 for advanced shells
│
├── victim/
│   ├── Dockerfile
│   ├── launcher.py               # Menu-driven shell launcher
│   └── shells/
│       ├── bash_revshell.sh
│       ├── nc_revshell.sh
│       ├── python_revshell.py
│       ├── php_revshell.php
│       └── encrypted_revshell.sh
│
├── detector/
│   ├── Dockerfile
│   ├── detector.py               # Main detection engine
│   ├── config.py                 # Thresholds & configuration
│   ├── models.py                 # SQLite models & schema
│   └── analyzers/
│       ├── heuristic.py
│       ├── statistical.py
│       └── signature.py
│
└── dashboard/
    ├── Dockerfile
    ├── app.py                    # Flask backend + WebSocket API
    ├── templates/
    │   └── index.html
    └── static/
        ├── css/style.css
        └── js/dashboard.js
```

---

## Configuration

Detection thresholds can be tuned in `detector/config.py`:

```python
# Packet size threshold for interactive session detection
INTERACTIVE_PKT_SIZE = 128        # bytes

# Minimum packets to classify as interactive session
MIN_INTERACTIVE_PACKETS = 10

# Entropy threshold for encrypted shell detection
ENTROPY_THRESHOLD = 7.0           # bits per byte (max 8.0)

# Beaconing detection interval tolerance
BEACON_INTERVAL_TOLERANCE = 0.15  # 15% variance

# Alert confidence thresholds
CONFIDENCE_LOW    = 0.30
CONFIDENCE_MEDIUM = 0.60
CONFIDENCE_HIGH   = 0.85
```

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only.**

ShellSnare is a controlled lab environment for studying network-based detection of reverse shell connections. All simulations run within isolated Docker containers on your local machine.

**Do not use the techniques or tools in this project against systems you do not own or have explicit authorization to test.** Unauthorized access to computer systems is illegal. The authors are not responsible for any misuse of this software.

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.
