# Ping Monitoring Tool

This Ping Monitoring Tool is a Python-based script designed to monitor the latency and availability of a list of hosts. It provides real-time updates on various metrics such as average latency, success rate, and jitter.

## Features

- **Real-time Monitoring**: Continuously monitors and displays ping statistics for a list of hosts.
- **Latency Tracking**: Tracks average latency, latency changes, and jitter.
- **Success Rate Calculation**: Calculates and displays the success rate of ping attempts.
- **Host Expansion**: Supports CIDR notation and IP ranges for bulk host monitoring.
- **Hostname Resolution**: Resolves and displays the hostname for each IP address.

## Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/saeed205/Network_Monitoring_Tool.git
   cd Network_Monitoring_Tool
   ```

2. **Install Dependencies**

   The required dependencies are listed in the `requirements.txt` file. You can install them using `pip`.

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare the Hosts List**

   Create a `hosts.txt` file in the root directory of the project. List the hosts you want to monitor, one per line. You can use individual IP addresses, CIDR notation, or IP ranges.

   Example `hosts.txt`:

   ```
   192.168.1.1
   192.168.1.5-192.168.1.10
   192.168.2.0/24
   google.com
   ```

2. **Run the Script**

   Execute the script using Python.

   ```sh
   python main.py
   ```

   The script will start monitoring the hosts listed in `hosts.txt` and display real-time statistics in the console.

## Code Explanation

### Main Components

1. **HostResult Class**: Stores and manages the ping statistics for each host.

2. **ping_host Function**: Continuously pings a host, updates its statistics, and stores the results in a shared dictionary.

3. **expand_hosts Function**: Expands CIDR notations and IP ranges into individual IP addresses.

4. **main Function**: Reads the hosts from the `hosts.txt` file, initializes the monitoring threads, and displays the real-time statistics using the Rich library.

### Ping Monitoring

- The script uses the `ping3` library to send ICMP ping requests to each host.
- The ping responses are recorded and analyzed to calculate various metrics:
  - **Response Time**: Time taken for the ping request to receive a response.
  - **Average Latency**: Average response time over the last 10 pings.
  - **Latency Change**: Indicates if the average latency has increased or decreased.
  - **Success Rate**: Percentage of successful ping responses.
  - **Jitter**: Difference between the maximum and minimum response times in the last 10 pings.

### Real-time Display

- The `rich` library is used to create a live-updating table in the console.
- The table displays the following columns:
  - Host
  - Hostname
  - Ping Response
  - Average Latency
  - Latency Change
  - Success Rate
  - Test Count
  - Last Update
  - Jitter

## Dependencies

- Python 3.x
- `ping3` library for sending ping requests
- `rich` library for creating the live-updating console table

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements or bug fixes.

## License

This project is licensed under the MIT License.