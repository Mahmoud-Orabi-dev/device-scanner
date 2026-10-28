import psutil
import platform
import json
import hashlib
import os
from datetime import datetime


def collect_system_info():
    return {
        "time": datetime.now().isoformat(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
    }


def collect_processes():
    procs = []
    for p in psutil.process_iter(["pid", "name", "exe", "username"]):
        try:
            info = p.info
            exe = info.get("exe")
            sha = None
            if exe and os.path.isfile(exe):
                try:
                    h = hashlib.sha256()
                    with open(exe, "rb") as f:
                        h.update(f.read(1024 * 1024))
                    sha = h.hexdigest()
                except Exception:
                    pass
            info["sha256_first_mb"] = sha
            procs.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return procs


def collect_connections():
    conns = []
    try:
        for c in psutil.net_connections(kind="inet"):
            if c.raddr:
                conns.append({
                    "pid": c.pid,
                    "local": f"{c.laddr.ip}:{c.laddr.port}",
                    "remote": f"{c.raddr.ip}:{c.raddr.port}",
                    "status": c.status,
                })
    except psutil.AccessDenied:
        pass
    return conns


if __name__ == "__main__":
    report = {
        "system": collect_system_info(),
        "processes": collect_processes(),
        "connections": collect_connections(),
    }
    with open("scan_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print("Processes:", len(report["processes"]))
    print("Connections:", len(report["connections"]))
    print("System:", report["system"])
