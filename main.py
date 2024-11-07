import time
import socket
import threading
from ping3 import ping
from rich.table import Table
from rich.console import Console
from rich.live import Live
from datetime import datetime
import ipaddress
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, List

class HostResult:
    """Stores the monitoring results for a single host."""

    def __init__(self, host: str, history_size: int = 10):
        self.host: str = host
        self.response: str = "unavailable"
        self.history: deque = deque(maxlen=history_size)
        self.avg_latency: float = 0.0
        self.latency_change: str = ""
        self.host_name: str = host
        self.success_rate: float = 0.0
        self.test_count: int = 0
        self.last_update: datetime = datetime.now()
        self.jitter: float = 0.0

    def update(self, latency: Optional[float]):
        """Updates the host result with the latest latency measurement."""
        self.test_count += 1
        self.last_update = datetime.now()

        if latency is None:
            self.response = "unavailable"
            self.history.append(None)
        else:
            latency_ms = latency * 1000  # Convert seconds to milliseconds
            self.response = f"{latency_ms:.2f} ms"
            self.history.append(latency_ms)

        self.calculate_metrics()

    def calculate_metrics(self):
        """Calculates average latency, jitter, success rate, and latency change."""
        non_none_history = [lat for lat in self.history if lat is not None]

        if non_none_history:
            new_avg = sum(non_none_history) / len(non_none_history)
            if self.avg_latency:
                if new_avg > self.avg_latency:
                    self.latency_change = "[red]↑[/]"
                elif new_avg < self.avg_latency:
                    self.latency_change = "[green]↓[/]"
                else:
                    self.latency_change = "-"
            self.avg_latency = new_avg
            self.jitter = max(non_none_history) - min(non_none_history)
            self.success_rate = (len(non_none_history) / len(self.history)) * 100
        else:
            self.avg_latency = 0.0
            self.jitter = 0.0
            self.success_rate = 0.0
            self.latency_change = "-"

class NetworkMonitor:
    """Monitors multiple hosts by continuously pinging them and displaying the results."""

    def __init__(self, hosts_file: str = "hosts.txt", ping_interval: float = 1.0, history_size: int = 10):
        self.hosts_file = hosts_file
        self.ping_interval = ping_interval
        self.history_size = history_size
        self.results: Dict[str, HostResult] = {}
        self.console = Console()
        self._load_hosts()

    def _load_hosts(self) -> List[str]:
        """Loads and expands the list of hosts from the hosts file."""
        try:
            with open(self.hosts_file, "r") as file:
                raw_hosts = [line.strip() for line in file if line.strip()]
            expanded_hosts = self._expand_hosts(raw_hosts)
            for host in expanded_hosts:
                self.results[host] = HostResult(host, self.history_size)
            return expanded_hosts
        except FileNotFoundError:
            self.console.print(f"[bold red]Error:[/] '{self.hosts_file}' file not found.")
            raise

    def _expand_hosts(self, hosts: List[str]) -> List[str]:
        """Expands CIDR notations and IP ranges into individual IP addresses."""
        expanded = []
        for host in hosts:
            if '/' in host:
                try:
                    network = ipaddress.IPv4Network(host, strict=False)
                    expanded.extend([str(ip) for ip in network.hosts()])
                except ValueError:
                    self.console.print(f"[yellow]Warning:[/] Invalid CIDR notation: {host}")
            elif '-' in host:
                try:
                    start_ip_str, end_ip_str = host.split('-')
                    start_ip = ipaddress.IPv4Address(start_ip_str.strip())
                    end_ip = ipaddress.IPv4Address(end_ip_str.strip())
                    if start_ip > end_ip:
                        self.console.print(f"[yellow]Warning:[/] Start IP {start_ip} is greater than end IP {end_ip}.")
                        continue
                    current_ip = start_ip
                    while current_ip <= end_ip:
                        expanded.append(str(current_ip))
                        current_ip += 1
                except ValueError:
                    self.console.print(f"[yellow]Warning:[/] Invalid IP range: {host}")
            else:
                expanded.append(host)
        return expanded

    def _resolve_hostname(self, host: str) -> str:
        """Resolves the hostname for a given IP address."""
        try:
            return socket.gethostbyaddr(host)[0]
        except socket.herror:
            return host

    def _ping_host(self, host: str):
        """Continuously pings a single host and updates its result."""
        host_result = self.results[host]
        host_result.host_name = self._resolve_hostname(host)

        while True:
            try:
                latency = ping(host, timeout=2)
            except Exception as e:
                self.console.print(f"[red]Error pinging {host}: {e}[/]")
                latency = None

            host_result.update(latency)
            time.sleep(self.ping_interval)

    def _start_pinging(self, hosts: List[str]):
        """Starts pinging all hosts using a thread pool."""
        with ThreadPoolExecutor(max_workers=len(hosts)) as executor:
            for host in hosts:
                executor.submit(self._ping_host, host)

    def _create_table(self) -> Table:
        """Creates a Rich table with the current monitoring results."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", justify="right")
        table.add_column("Host")
        table.add_column("Hostname")
        table.add_column("Ping Response")
        table.add_column("Average Latency")
        table.add_column("Latency Change")
        table.add_column("Success Rate")
        table.add_column("Test Count")
        table.add_column("Last Update")
        table.add_column("Jitter")

        for idx, host in enumerate(self.results.keys(), start=1):
            result = self.results[host]
            table.add_row(
                str(idx),
                result.host,
                result.host_name,
                result.response,
                f"{result.avg_latency:.2f} ms" if result.avg_latency else "N/A",
                result.latency_change or "-",
                f"{result.success_rate:.2f} %" if result.history else "0.00 %",
                str(result.test_count),
                result.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                f"{result.jitter:.2f} ms" if result.jitter else "0.00 ms"
            )

        return table

    def display(self):
        """Displays the live-updating table of monitoring results."""
        with Live(self._create_table(), refresh_per_second=1, console=self.console) as live:
            while True:
                live.update(self._create_table())
                time.sleep(1)

    def run(self):
        """Runs the network monitor."""
        try:
            hosts = list(self.results.keys())
            if not hosts:
                self.console.print("[bold yellow]No hosts to monitor.[/]")
                return

            threading.Thread(target=self._start_pinging, args=(hosts,), daemon=True).start()
            self.display()
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Monitoring stopped by user.[/]")

def main():
    monitor = NetworkMonitor(hosts_file="hosts.txt", ping_interval=1.0, history_size=10)
    monitor.run()

if __name__ == "__main__":
    main()
