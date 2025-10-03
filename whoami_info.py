# whoami_info.py
import socket
import platform
import uuid
import sys
import subprocess

def get_hostname():
    return socket.gethostname()

def get_local_ips():
    ips = set()
    try:
        # gethostname may not resolve to all interfaces, so gather via getaddrinfo
        for res in socket.getaddrinfo(socket.gethostname(), None):
            addr = res[4][0]
            # skip IPv6 link-local and loopback
            if not addr.startswith("127.") and ':' not in addr:
                ips.add(addr)
    except Exception:
        pass

    # fallback: connect to an external host (no data sent) to learn the outbound IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass

    return list(ips) or ["Unknown"]

def get_mac_addresses():
    mac = uuid.getnode()
    # If uuid.getnode() returns a random value, it may not be a real MAC; convert anyway
    mac_str = ':'.join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    return [mac_str]

def get_public_ip():
    # Try to fetch public IP using curl or dig; works if internet and curl present.
    # We'll try curl, then dig, else return Unknown.
    try:
        out = subprocess.check_output(["curl", "-s", "https://ifconfig.me"], stderr=subprocess.DEVNULL, timeout=5)
        ip = out.decode().strip()
        if ip:
            return ip
    except Exception:
        pass
    try:
        out = subprocess.check_output(["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"], stderr=subprocess.DEVNULL, timeout=5)
        ip = out.decode().strip()
        if ip:
            return ip
    except Exception:
        pass
    return "Unknown (no curl/dig or offline)"

if __name__ == "__main__":
    print("=== System Info ===")
    print("Hostname :", get_hostname())
    print("Platform :", platform.system(), platform.release())
    print("Machine  :", platform.machine())
    print()
    print("=== Network Info ===")
    ips = get_local_ips()
    for i, ip in enumerate(ips, 1):
        print(f"Local IP {i}:", ip)
    macs = get_mac_addresses()
    for i, mac in enumerate(macs, 1):
        print(f"MAC {i}    :", mac)
    print("Public IP :", get_public_ip())
