import ipaddress
import queue
import subprocess
import threading

Target = input("Enter the target network range: ")
queue_hosts = queue.Queue()
print_lock = threading.Lock()
Active_hosts = []

try:
    network = ipaddress.ip_network(Target, strict=False)
    for ip in network.hosts():
        queue_hosts.put(str(ip))
except ValueError as e:
    print(f"[+] Invalid network range: {e}")

def check_host(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", str(ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False

def worker():
    while True:
        ip = queue_hosts.get()
        if check_host(ip):
            with print_lock:
                print(f"[+] Active host found: {ip}")
                Active_hosts.append(ip)
        queue_hosts.task_done()

if __name__ == "__main__":
    Thread_count = 100
    print(f"[DEBUG] Target input received: {Target}")
    print(f"[DEBUG] Queue size: {queue_hosts.qsize()}")
    print(f"Starting ping sweep on target network: {Target}\n")
    
    for _ in range(Thread_count):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        
    queue_hosts.join()
    print("\n[+] Ping Sweep Completed!")