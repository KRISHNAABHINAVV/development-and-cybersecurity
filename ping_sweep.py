# ping_sweep.py
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    # suppress output, check return code
    try:
        res = subprocess.run(["ping", param, "1", "-W", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return ip, res.returncode == 0
    except Exception:
        return ip, False

def sweep(base_ip_prefix="192.168.1."):
    live = []
    with ThreadPoolExecutor(max_workers=100) as ex:
        futures = [ex.submit(ping, base_ip_prefix + str(i)) for i in range(1, 255)]
        for f in as_completed(futures):
            ip, ok = f.result()
            if ok:
                live.append(ip)
    return sorted(live)

if __name__ == "__main__":
    # change prefix to match your LAN (find from ifconfig/ipconfig)
    prefix = input("Enter subnet prefix (e.g., 192.168.1.): ").strip() or "192.168.1."
    print("Scanning", prefix + "1-254 (this may take a few seconds)...")
    found = sweep(prefix)
    print("Live hosts:")
    for ip in found:
        print(" -", ip)
