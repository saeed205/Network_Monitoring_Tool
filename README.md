# Ping Monitoring Tool

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)

The **Ping Monitoring Tool** is a robust Python-based script designed to continuously monitor the latency and availability of multiple hosts. It offers real-time insights into various performance metrics, including average latency, success rate, and jitter, presented through a dynamic console interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Preparing the Hosts List](#preparing-the-hosts-list)
  - [Running the Monitor](#running-the-monitor)
- [Configuration](#configuration)
- [Code Overview](#code-overview)
  - [Main Components](#main-components)
  - [Metrics Tracked](#metrics-tracked)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Real-time Monitoring**: Continuously monitors and displays ping statistics for a list of hosts.
- **Latency Tracking**: Tracks average latency, latency changes, and jitter over a configurable history size.
- **Success Rate Calculation**: Calculates and displays the success rate of ping attempts.
- **Host Expansion**: Supports CIDR notation and IP ranges for bulk host monitoring.
- **Hostname Resolution**: Resolves and displays the hostname for each IP address.
- **Dynamic Console Display**: Utilizes the Rich library to present real-time, live-updating tables in the console.
- **Graceful Shutdown**: Handles user interruptions gracefully, ensuring clean termination of monitoring threads.
- **Configurable Parameters**: Allows customization of ping intervals and history sizes to suit various monitoring needs.

## Installation

### 1. Clone the Repository

Begin by cloning the repository to your local machine:

```sh
git clone https://github.com/saeed205/Network_Monitoring_Tool.git
cd Network_Monitoring_Tool
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps manage dependencies and maintain project isolation.

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```sh
pip install -r requirements.txt
```

**Note**: Ensure you have Python 3.x installed on your system.

## Usage

### Preparing the Hosts List

Create a `hosts.txt` file in the root directory of the project. List the hosts you want to monitor, one per line. You can specify hosts using individual IP addresses, CIDR notation, or IP ranges.

**Example `hosts.txt`:**

```
192.168.1.1
192.168.1.5-192.168.1.10
192.168.2.0/24
google.com
```

**Host Specification Formats:**

- **Single IP Address**: `192.168.1.1`
- **IP Range**: `192.168.1.5-192.168.1.10`
- **CIDR Notation**: `192.168.2.0/24`
- **Hostname**: `google.com`

### Running the Monitor

Execute the script using Python:

```sh
python main.py
```

Upon running, the script will start monitoring the hosts listed in `hosts.txt` and display real-time statistics in the console.

**Sample Console Output:**

![Sample Output](https://i.imgur.com/YourImageLink.png) *(Replace with an actual screenshot if available)*

**Stopping the Monitor:**

- Press `Ctrl+C` to gracefully terminate the monitoring process.

## Configuration

The tool allows you to customize key parameters to fit your monitoring requirements. These can be adjusted in the `NetworkMonitor` class within the `main.py` script.

- **Ping Interval**: Time between successive pings (default: `1.0` seconds).
- **History Size**: Number of recent ping results to consider for metrics calculation (default: `10`).

**Example:**

```python
monitor = NetworkMonitor(hosts_file="hosts.txt", ping_interval=2.0, history_size=20)
```

## Code Overview

### Main Components

1. **HostResult Class**
   - **Purpose**: Stores and manages the ping statistics for each host.
   - **Attributes**:
     - `host`: IP address or hostname.
     - `host_name`: Resolved hostname.
     - `response`: Latest ping response time or status.
     - `history`: Fixed-size history of recent ping results.
     - `avg_latency`: Average latency over the history.
     - `latency_change`: Indicator of latency trend (increase/decrease).
     - `success_rate`: Percentage of successful pings.
     - `test_count`: Total number of ping attempts.
     - `last_update`: Timestamp of the last ping.
     - `jitter`: Difference between max and min latency in history.

2. **NetworkMonitor Class**
   - **Purpose**: Manages the overall monitoring process, including host expansion, pinging, and display.
   - **Key Methods**:
     - `_load_hosts()`: Loads and expands hosts from `hosts.txt`.
     - `_expand_hosts(hosts)`: Expands CIDR notations and IP ranges.
     - `_resolve_hostname(host)`: Resolves IP addresses to hostnames.
     - `_ping_host(host)`: Continuously pings a single host and updates its statistics.
     - `_start_pinging(hosts)`: Initiates pinging for all hosts using a thread pool.
     - `_create_table()`: Generates the dynamic console table using Rich.
     - `display()`: Handles the live display of monitoring data.
     - `run()`: Starts the monitoring process.

### Metrics Tracked

- **Response Time**: Time taken for each ping response.
- **Average Latency**: Mean response time over the defined history size.
- **Latency Change**: Visual indicator showing if latency is increasing or decreasing.
- **Success Rate**: Ratio of successful pings to total attempts.
- **Jitter**: Variability in latency (max - min over history).
- **Test Count**: Total number of ping attempts per host.
- **Last Update**: Timestamp of the most recent ping.
  
## Dependencies

- **Python 3.x**: Programming language used for the script.
- **[ping3](https://pypi.org/project/ping3/)**: Library for sending ICMP ping requests.
- **[Rich](https://pypi.org/project/rich/)**: Library for creating rich text and beautiful formatting in the console.

**Installation via `requirements.txt`:**

```sh
pip install -r requirements.txt
```

## Contributing

Contributions are highly welcome! Whether it's reporting bugs, suggesting enhancements, or submitting pull requests, your involvement helps improve the tool.

### How to Contribute

1. **Fork the Repository**

   Click the "Fork" button at the top right of the repository page to create a copy of the project in your GitHub account.

2. **Clone Your Fork**

   ```sh
   git clone https://github.com/your-username/Network_Monitoring_Tool.git
   cd Network_Monitoring_Tool
   ```

3. **Create a New Branch**

   ```sh
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

   Implement your feature or bug fix.

5. **Commit Your Changes**

   ```sh
   git commit -m "Add feature: Description of your feature"
   ```

6. **Push to Your Fork**

   ```sh
   git push origin feature/YourFeatureName
   ```

7. **Submit a Pull Request**

   Navigate to the original repository and click on "Compare & pull request" to submit your changes for review.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the license terms.

---

## Additional Recommendations

1. **Add a `LICENSE` File**:
   Ensure you have a `LICENSE` file in your repository containing the full text of the MIT License.

2. **Include Screenshots**:
   Visual aids can help users understand what to expect when running the tool. Consider adding screenshots of the console output.

3. **Provide Example Output**:
   Including snippets of sample output in the README can give users a quick preview of the tool's functionality.

4. **Enhance Error Handling Documentation**:
   Document common errors and troubleshooting steps to assist users in resolving potential issues.

5. **Automate Testing**:
   Incorporate tests to ensure the reliability of your tool. You can mention testing instructions in the README if applicable.

6. **Continuous Integration**:
   Set up CI/CD pipelines (e.g., GitHub Actions) to automate testing and deployment processes.
