from scapy.all import ARP, Ether, srp, conf
import sys

def arp_scan(target_ip):
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=target_ip)
    packet = ether / arp
    result, _ = srp(packet, timeout=3, verbose=False)
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

if __name__ == "__main__":
    print(f"[*] Active Default Interface: {conf.iface}")
    print("[*] ARP Network Scanner Initialized")
    target_ip = input("Enter target subnet: ")
    
    print(f"\n[+] Broadcasting ARP requests across {target_ip}...")
    active_hosts = arp_scan(target_ip)
    
    print(f"\n[+] Scan complete. Discovered {len(active_hosts)} live host(s):\n")
    if active_hosts:
        print(f"{'IP Address':<18} | {'MAC Address'}")
        print("-" * 35)
        for device in active_hosts:
            print(f"{device['ip']:<18} | {device['mac']}")
    else:
        print("[-] No live hosts found. Make sure you are using the correct subnet range.")