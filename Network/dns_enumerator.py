import socket
import concurrent.futures
import sys
import os

def load_wordlist(filepath):
    if not os.path.exists(filepath):
        print(f"[-] Error: Wordlist file '{filepath}' not found.")
        sys.exit(1)
    
    print(f"[*] Loading wordlist from: {filepath}")
    with open(filepath, 'r', encoding='latin-1') as f:
        wordlist = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    print(f"[*] Loaded {len(wordlist)} subdomains from file.")
    return wordlist

def resolve_subdomain(domain, sub):
    full_domain = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return (full_domain, ip)
    except socket.gaierror:
        return None

def dns_enumerate(domain, wordlist, max_threads=50):
    print(f"\n[+] Enumerating subdomains for target: {domain}\n")
    print(f"{'Subdomain Target':<35} | {'Resolved IP Address'}")
    print("-" * 60)

    discovered = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(resolve_subdomain, domain, sub): sub for sub in wordlist}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                sub_domain, ip = result
                print(f"{sub_domain:<35} | {ip}")
                discovered += 1

    print(f"\n[+] Enumeration complete. Discovered {discovered} active subdomain(s).")

if __name__ == "__main__":
    default_words = ["www", "mail", "ftp", "localhost", "webmail", "admin", "dev", "api", "test", "staging", "portal", "vpn"]
    
    target_domain = sys.argv[1] if len(sys.argv) > 1 else input("Enter target domain (e.g., example.com): ").strip()
    wordlist_path = sys.argv[2] if len(sys.argv) > 2 else input("Enter wordlist path (leave blank for default small list): ").strip()

    if not target_domain:
        print("[-] Error: Target domain cannot be empty.")
        sys.exit(1)

    if wordlist_path:
        wordlist = load_wordlist(wordlist_path)
    else:
        print("[*] Using built-in default wordlist...")
        wordlist = default_words

    try:
        dns_enumerate(target_domain, wordlist)
    except KeyboardInterrupt:
        print("\n[-] Scan aborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"[-] Error: {e}")