import platform
import queue
import socket
import struct
import threading
import time

THREAD_COUNT = 100 
packet_inbox = queue.Queue()
print_lock = threading.Lock()

def packet_capture_linux():
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while True:
        packet, addr = s.recvfrom(65535)
        packet_inbox.put(packet)

def packet_capture_windows():
    HOST = input('Enter your local IP address: ') 
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((HOST, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    while True:
        packet, addr = s.recvfrom(65535)
        packet_inbox.put(packet)

def packet_worker():
    while True:
        packet = packet_inbox.get()
        iph = packet[0:20]
        unpacked_iph = struct.unpack("!BBHHHBBH4s4s", iph)
        
        src_ip = socket.inet_ntoa(unpacked_iph[8])
        dst_ip = socket.inet_ntoa(unpacked_iph[9])
        protocol = unpacked_iph[6]
        
        is_anomaly = False
        anomaly_reason = ""
        if protocol not in [6, 17]:
            is_anomaly = True
            anomaly_reason = f"Uncommon Protocol Detected : ({protocol})"
            
        with print_lock:
            if is_anomaly:
                print(f"[!] ANOMALY: {anomaly_reason} | Sender: {src_ip} -> Destination: {dst_ip}")
            else:
                print(f"Normal | Sender: {src_ip} | Destination: {dst_ip} | Protocol: {protocol}")
                
        packet_inbox.task_done()

if __name__ == "__main__":
    print("[*] Engine is running! Open a browser and visit a website to generate packets...")
    x = input("If you have linux type 1, if you have windows type 2: ")
    
    if x == "1":
        capture_target = packet_capture_linux
    elif x == "2":
        capture_target = packet_capture_windows
    else:
        if platform.system() == "Windows":
            capture_target = packet_capture_windows
        else:
            capture_target = packet_capture_linux

    capture_thread = threading.Thread(target=capture_target, daemon=True)
    capture_thread.start()
    
    for _ in range(THREAD_COUNT - 1):
        t = threading.Thread(target=packet_worker, daemon=True)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping packet sniffer...")