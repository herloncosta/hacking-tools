import argparse
import socket
import threading
from queue import Queue
import json
import csv


def parse_ports(port_range_str):
    """Parses port ranges like '20-80' into a range object."""
    start, end = map(int, port_range_str.split('-'))
    return range(start, end + 1)


def scan_port(target, port, timeout, verbose, grab_banner, open_ports):
    """Attempts to connect to a target port and optionally grabs a banner."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                banner = ""
                if grab_banner:
                    try:
                        banner = s.recv(1024).decode(
                            'utf-8', errors='ignore').strip()
                    except Exception:
                        banner = "N/A"
                open_ports.append({
                    "target": target,
                    "port": port,
                    "status": "open",
                    "banner": banner
                })
                if verbose:
                    print(f"[+] {port}/tcp open - {banner}")
            elif verbose:
                print(f"[-] {port}/tcp closed")
    except Exception as e:
        if verbose:
            print(f"[!] Error on port {port}: {e}")


def run_scanner(target, port_range, num_threads, timeout, verbose, grab_banner):
    """Manages the thread pool and port scanning."""
    port_queue = Queue()
    open_ports = []

    for port in port_range:
        port_queue.put(port)

    def worker():
        while not port_queue.empty():
            port = port_queue.get()
            scan_port(target, port, timeout, verbose, grab_banner, open_ports)
            port_queue.task_done()

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return sorted(open_ports, key=lambda x: x['port'])


def export_results(results, filename):
    """Exports the scan results to a JSON or CSV file."""
    if filename.endswith('.json'):
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
    elif filename.endswith('.csv'):
        keys = results[0].keys() if results else [
            "target", "port", "status", "banner"]
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
    else:
        print(f"[!] Unsupported file format: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="⚡ Port Scanner com Banner Grabbing + Exportação")
    parser.add_argument("-t", "--target", required=True,
                        help="IP ou hostname do alvo")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Intervalo de portas (ex: 1-65535)")
    parser.add_argument("--threads", type=int, default=100,
                        help="Número de threads")
    parser.add_argument("--timeout", type=float, default=1.0,
                        help="Timeout por conexão (em segundos)")
    parser.add_argument("--verbose", action="store_true",
                        help="Exibir progresso do scanner")
    parser.add_argument("--banners", action="store_true",
                        help="Ativar captura de banners")
    parser.add_argument("--output", help="Arquivo de saída (.json ou .csv)")

    args = parser.parse_args()

    port_range = parse_ports(args.ports)
    open_ports = run_scanner(
        args.target, port_range, args.threads,
        args.timeout, args.verbose, args.banners
    )

    print(f"\n[✔] Portas abertas encontradas em {args.target}:")
    for entry in open_ports:
        print(
            f"    - {entry['port']}/tcp open | {entry['banner'] if entry['banner'] else 'No banner'}")

    if args.output:
        export_results(open_ports, args.output)
        print(f"\n[💾] Resultados exportados para {args.output}")


if __name__ == "__main__":
    main()
