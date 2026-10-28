# Device Scanner

A Python tool that scans a device for suspicious processes and network connections.

## Features

- Collects basic system information (OS, CPU, RAM)
- Lists all running processes with their executable paths
- Computes a SHA-256 hash for each executable
- Lists active network connections and the process behind each one
- Saves everything to a JSON report

## Requirements

- Python 3.8 or newer
- psutil library

## Installation

    pip install psutil

## Usage

    python scanner.py

The scan results are saved to scan_report.json in the same folder.

## Roadmap

- Compare file hashes against known malware databases
- Add AI-based anomaly detection
- Build a simple user interface

## Author

Mahmoud Orabi Elnagar
