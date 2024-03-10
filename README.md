# DNS Monitoring Service

This project provides a DNS monitoring service using Python. It continuously monitors the performance and reliability of a set of DNS services, and generates metrics that can be used for alerting or performance tuning.

## Files

- `dnsresolver.py`: This script is a DNS resolver that monitors the status of a DNS server. It sets up two metrics, `dns_packet_loss` and `dns_response_time`, to monitor the packet loss percentage and response time of the DNS server.

- `main.py`: This script is the main driver for the DNS monitoring service. It reads DNS services from a YAML file named `newdns.yaml`, and performs DNS discovery and monitors the DNS services at regular intervals.

## Usage

1. Ensure you have the necessary Python packages installed. You can install them with pip:

    ```bash
    pip install -r requirements.txt

    requirements:
    requests
    pyyaml
    dnspython
    prometheus_client

    ```

2. Update the `newdns.yaml` file with the DNS services you want to monitor.

3. Run the main script:

    ```bash
    python main.py
    ```

The service will start a Prometheus server and begin monitoring the DNS services. If the program is interrupted (e.g., by a keyboard interrupt), it will print a message and exit.

## Metrics

The service generates the following metrics:

- `dns_packet_loss`: The packet loss percentage of the DNS server.
- `dns_response_time`: The response time of the DNS server in milliseconds.

These metrics are exposed on a Prometheus endpoint, and can be scraped by a Prometheus server for further analysis and alerting.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
