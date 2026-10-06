import queue
import socket
import subprocess
import sys
import threading

THREAD_COUNT = 50
port_queue = queue.Queue()
print_lock = threading.Lock()

def grab_banner(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((target_ip, port))
        
        if port in [80, 443, 8080, 8443]:
            try:
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            except:
                pass
                
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        
        with print_lock:
            if banner:
                print(f"[+] Port {port} OPEN | Banner: {banner}")
            else:
                print(f"[+] Port {port} OPEN | No banner returned")
    except Exception:
        pass
    finally:
        port_queue.task_done()

def worker(target_ip):
    while True:
        port = port_queue.get()
        grab_banner(target_ip, port)

if __name__ == "__main__":
    print("[*] Banner Grabber Orchestrator Initialized")
    target_ip = input("Enter the target IP address: ")

    print(f"\n[+] Executing the port scanner for {target_ip}...")
    
    process = subprocess.run(
        [sys.executable, "port_scanner.py"],
        input=target_ip + "\n",
        capture_output=True,
        text=True
    )

    open_ports = []
    for line in process.stdout.splitlines():
        if "open" in line.lower() or "+" in line:
            words = line.split()
            for word in words:
                if word.isdigit():
                    open_ports.append(int(word))
                    break

    open_ports = sorted(list(set(open_ports)))
    print(f"[+] Port scanning finished. Found {len(open_ports)} open ports: {open_ports}")

    if not open_ports:
        print("[-] No open ports found . Exiting.")
        sys.exit(0)

    for port in open_ports:
        port_queue.put(port)

    print(f"\n[+] Starting Banner Grabbing on discovered ports...\n")
    
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=worker, args=(target_ip,), daemon=True)
        t.start()

    port_queue.join()
    print("\n[*] Banner grabbing complete!")