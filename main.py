import time
import socket
import threading
from ping3 import ping
from rich.table import Table
from rich.console import Console
from rich.live import Live
from datetime import datetime

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
        self.jitter = 0  # Added for keeping track of jitter

def ping_host(host, results):
    host_result = HostResult(host)
    try:
        host_result.host_name = socket.gethostbyaddr(host)[0]
    except Exception:
        pass

    while True:
        ms = ping(host)
        host_result.test_count += 1
        host_result.last_update = datetime.now()

        if ms is None:
            host_result.response = "unavailable"
            host_result.history.append(None)
        else:
            host_result.response = "{} ms".format(ms)
            host_result.history.append(ms)

        if len(host_result.history) > 10:
            host_result.history = host_result.history[1:]

        non_none_history = [i for i in host_result.history if i is not None]
        if non_none_history:
            avg_latency = sum(non_none_history) / len(non_none_history)
            if host_result.avg_latency and avg_latency > host_result.avg_latency:
                host_result.latency_change = "[red]↑[/]"
            elif host_result.avg_latency and avg_latency < host_result.avg_latency:
                host_result.latency_change = "[green]↓[/]"
            host_result.avg_latency = avg_latency

            # Calculate the jitter
            host_result.jitter = max(non_none_history) - min(non_none_history)

        # Calculate the success rate of the last 10 pings
        successful_pings = len([h for h in host_result.history if h is not None])
        host_result.success_rate = successful_pings / len(host_result.history) * 100

        results[host] = host_result
        time.sleep(1)

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <ip_address_1> <ip_address_2> ...")
        return

    hosts = sys.argv[1:]
    results = {}

    for host in hosts:
        threading.Thread(target=ping_host, args=(host, results)).start()

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
                        str(i+1), 
                        result.host, 
                        result.host_name, 
                        result.response, 
                        "{:.2f} ms".format(result.avg_latency if result.avg_latency else 0), 
                        result.latency_change,
                        "{:.2f} %".format(result.success_rate),
                        str(result.test_count),
                        result.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                        "{:.2f} ms".format(result.jitter)
                    ]
                    table.add_row(*row)
            live.update(table)

if __name__ == "__main__":
    main()
