import socket 
import threading
import queue

TARGET_IP = input("Enter the target IP address here: ")
THREAD_COUNT = 100 

port_inbox = queue.Queue()
print_lock = threading.Lock()

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        status = s.connect_ex((TARGET_IP, port))
        s.close()
        return status == 0
    except socket.error:
        return False

def thread_scan():
    while True:
        port = port_inbox.get()
        if scan_port(port):
            with print_lock:
                print(f"[*] Port {port} is OPEN")
        port_inbox.task_done()

if __name__ == "__main__":
    print(f"Starting scan on target: {TARGET_IP}")
    
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=thread_scan)
        t.daemon = True 
        t.start()

    for number in range(1, 65536):
        port_inbox.put(number)

    port_inbox.join()
    print("\nScan Complete!")