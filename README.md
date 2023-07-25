# Network Monitoring Tool

This is a simple network monitoring tool written in Python. It pings the specified hosts continuously and provides real-time latency, success rate, jitter, and other details in a neatly formatted table. The tool utilizes the `ping3` package for pinging the hosts and the `rich` library for the display of results.

## Features

- Ping multiple hosts simultaneously
- Calculate average latency of the last 10 pings
- Show latency change (increase or decrease) based on the average latency
- Calculate success rate based on the last 10 pings
- Calculate the number of total ping tests performed
- Show the timestamp of the last ping test
- Calculate jitter, which is the difference between the maximum and minimum latency values over the last 10 successful pings

## Prerequisites

To run this tool, you need Python 3.6 or later. The required packages can be installed with:

```
pip install ping3 rich
```

## Usage

To use this tool, provide the IP addresses or hostnames as arguments when running the script:

```
python main.py 8.8.8.8 8.8.4.4
```

This will start pinging the Google DNS servers and present the result in a continuously updating table:

```
┏━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┓
┃ # ┃ Host   ┃ Hostname         ┃ Ping Response┃ Average Latency┃ Latency Change ┃ Success Rate┃ Test Count┃ Last Update   ┃ Jitter ┃
┡━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━┩
│ 1 │8.8.8.8 │dns.google        │9.58 ms      │9.58 ms         │               │100.00 %     │1          │2023-07-25 14:25:26│0.00 ms│
│ 2 │8.8.4.4 │dns.google        │11.24 ms     │11.24 ms        │               │100.00 %     │1          │2023-07-25 14:25:26│0.00 ms│
└───┴────────┴──────────────────┴─────────────┴─────────────────┴───────────────┴─────────────┴───────────┴───────────────┴───────┘
```

## Explanation

The script starts by taking IP addresses or hostnames as arguments. For each host, it starts a separate thread that continuously pings the host and updates the host's results in the shared results dictionary.

The `HostResult` class is used to store the results for a host. It includes the host's IP address or hostname, the latest ping response, a history of the last 10 ping latencies, the average latency, an indicator of latency change, the calculated success rate, the total number of ping tests performed, the timestamp of the last ping test, and the calculated jitter.

The `ping_host` function is responsible for continuously pinging a host and updating the host's result. It pings the host using the `ping3` package, records the latency, calculates the average latency, determines if the latency has increased or decreased compared to the previous average latency, calculates the success rate, counts the total number of tests, records the timestamp of the last test, and calculates the jitter.

The `main` function starts the pinging threads and continuously updates the display table with the latest results using the `rich` library.
