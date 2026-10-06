import socket
import struct
import time
import sys

def checksum(source_string):
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0
    while count < count_to:
        val = source_string[count + 1] * 256 + source_string[count]
        sum += val
        sum &= 0xffffffff
        count += 2
    if count_to < len(source_string):
        sum += source_string[-1]
        sum &= 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum
    answer &= 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_icmp_packet(packet_id):
    header = struct.pack('bbHHh', 8, 0, 0, packet_id, 1)
    data = struct.pack('d', time.time())
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', 8, 0, socket.htons(my_checksum), packet_id, 1)
    return header + data

def traceroute(dest_name, max_hops=30, timeout=2.0):
    dest_addr = socket.gethostbyname(dest_name)
    icmp_proto = socket.getprotobyname('icmp')
    
    print(f"\n[+] Tracing route to {dest_name} ({dest_addr}) with a max of {max_hops} hops:\n")
    print(f"{'Hop':<4} | {'IP Address':<18} | {'RTT (ms)'}")
    print("-" * 42)

    for ttl in range(1, max_hops + 1):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
        recv_socket.settimeout(timeout)
        recv_socket.bind(("", 33434))
        
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
        send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        
        packet_id = (id(None) + ttl) & 0xFFFF
        packet = create_icmp_packet(packet_id)
        
        t_start = time.time()
        try:
            send_socket.sendto(packet, (dest_addr, 33434))
            curr_addr = None
            curr_name = None
            while True:
                try:
                    data, curr_addr = recv_socket.recvfrom(512)
                    curr_addr = curr_addr[0]
                    t_end = time.time()
                    rtt = (t_end - t_start) * 1000.0
                    break
                except socket.timeout:
                    rtt = None
                    break
        finally:
            send_socket.close()
            recv_socket.close()

        if curr_addr:
            print(f"{ttl:<4} | {curr_addr:<18} | {rtt:.2f} ms")
            if curr_addr == dest_addr:
                print(f"\n[+] Destination reached at hop {ttl}.")
                break
        else:
            print(f"{ttl:<4} | {'* * * Request timed out':<18} | ")

if __name__ == "__main__":
    target = input("Enter target domain or IP (e.g., 8.8.8.8): ")
    try:
        traceroute(target)
    except PermissionError:
        print("[-] Error: Raw sockets require root privileges. Run with sudo.")
    except Exception as e:
        print(f"[-] Error: {e}")