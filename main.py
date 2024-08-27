import time
import socket
import threading
from ping3 import ping
from rich.table import Table
from rich.console import Console
from rich.live import Live
from datetime import datetime
import ipaddress

class HostResult:
    def __init__(self, host):
        self.host = host
        self.response = "unavailable"
        self.history = []
        self.avg_latency = 0
        self.latency_change = ""
        self.host_name = host
        self.success_rate = 0
        self.test_count = 0
        self.last_update = datetime.now()
        self.jitter = 0

def ping_host(host, results):
    host_result = HostResult(host)
    try:
        host_result.host_name = socket.gethostbyaddr(host)[0]
    except socket.herror:
        pass

    while True:
        ms = ping(host, timeout=2)
        host_result.test_count += 1
        host_result.last_update = datetime.now()

        if ms is None:
            host_result.response = "unavailable"
            host_result.history.append(None)
        else:
            ms = ms * 100 * 10
            host_result.response = f"{ms:.2f} ms"
            host_result.history.append(ms)

        if len(host_result.history) > 10:
            host_result.history.pop(0)

        non_none_history = [i for i in host_result.history if i is not None]
        if non_none_history:
            avg_latency = sum(non_none_history) / len(non_none_history)
            if host_result.avg_latency:
                if avg_latency > host_result.avg_latency:
                    host_result.latency_change = "[red]↑[/]"
                elif avg_latency < host_result.avg_latency:
                    host_result.latency_change = "[green]↓[/]"
            host_result.avg_latency = avg_latency

            host_result.jitter = max(non_none_history) - min(non_none_history)

        successful_pings = len(non_none_history)
        host_result.success_rate = (successful_pings / len(host_result.history)) * 100

        results[host] = host_result
        time.sleep(1)

def expand_hosts(hosts):
    expanded_hosts = []
    for host in hosts:
        if '/' in host:
            try:
                expanded_hosts.extend([str(ip) for ip in ipaddress.IPv4Network(host, strict=False)])
            except ValueError:
                print(f"Invalid CIDR notation: {host}")
        elif '-' in host:
            try:
                start_ip_str, end_ip_str = host.split('-')
                start_ip = ipaddress.IPv4Address(start_ip_str.strip())
                end_ip = ipaddress.IPv4Address(end_ip_str.strip())
                if start_ip <= end_ip:
                    current_ip = start_ip
                    while current_ip <= end_ip:
                        expanded_hosts.append(str(current_ip))
                        current_ip += 1
                else:
                    print(f"Invalid IP range: {host}")
            except ValueError:
                print(f"Invalid IP range: {host}")
        else:
            expanded_hosts.append(host)
    return expanded_hosts

def main():
    try:
        with open("hosts.txt", "r") as file:
            hosts = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: 'hosts.txt' file not found.")
        return

    hosts = expand_hosts(hosts)
    results = {}

    for host in hosts:
        threading.Thread(target=ping_host, args=(host, results), daemon=True).start()

    console = Console()
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("#")
            table.add_column("Host")
            table.add_column("Hostname")
            table.add_column("Ping Response")
            table.add_column("Average Latency")
            table.add_column("Latency Change")
            table.add_column("Success Rate")
            table.add_column("Test Count")
            table.add_column("Last Update")
            table.add_column("Jitter")

            for i, host in enumerate(hosts):
                if host in results:
                    result = results[host]
                    row = [
                        str(i + 1),
                        result.host,
                        result.host_name,
                        result.response,
                        f"{result.avg_latency:.2f} ms",
                        result.latency_change,
                        f"{result.success_rate:.2f} %",
                        str(result.test_count),
                        result.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                        f"{result.jitter:.2f} ms"
                    ]
                    table.add_row(*row)

            live.update(table)
            time.sleep(1)

if __name__ == "__main__":
    main()
