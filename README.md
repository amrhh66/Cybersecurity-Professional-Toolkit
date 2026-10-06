# 🛡️ Cybersecurity-Professional-Toolkit

A collection of custom-built Python networking, system auditing, and security tools designed from scratch for efficiency, automation, and practical security testing.

---

## 🧰 Included Tools

| Tool | File | Description |
| :--- | :--- | :--- |
| **Layer 2 ARP Local Host Discovery** | `Network/arp_scanner.py` | A low-level network reconnaissance utility using Scapy to broadcast Layer 2 ARP frames across a target subnet, bypassing ICMP/ping blocks to discover live hosts and their MAC addresses. |
| **Service Banner Grabber Orchestrator** | `Network/banner_grabber.py` | An automated recon utility that explicitly invokes `port_scanner.py` as a subprocess, parses its output for open ports, and deploys a multi-threaded queue to extract service banners and version strings. |
| **Multithreaded Packet Sniffer & Anomaly Detector** | `Network/packet_sniffer.py` | A low-level, multithreaded raw socket packet sniffer and intrusion detection utility that captures network traffic across OS platforms, parses IP/TCP headers via struct unpacking, and flags protocol anomalies in real-time. |
| **Subnet Host Discovery (Ping Sweep)** | `Network/ping_sweep.py` | A multithreaded network discovery tool that uses a queue-based architecture and subprocess ping checks to rapidly identify active hosts across a target subnet. |
| **Multithreaded TCP Port Scanner** | `Network/port_scanner.py` | A high-performance, queue-based TCP port scanner that checks all 65,535 ports concurrently using worker threads, custom timeouts, and thread-safe terminal printing. |

---

## 🚀 Getting Started

Clone the repository to your local machine:

```bash
git clone [https://github.com/amrhh66/CyberSecurity-Professional-Toolkit.git](https://github.com/amrhh66/CyberSecurity-Professional-Toolkit.git)
cd CyberSecurity-Professional-Toolkit