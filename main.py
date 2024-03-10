from datetime import datetime, timedelta
from time import sleep
import requests
import yaml
from dnsresolver import dnsmonitor, dns_loss, dns_time
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import Gauge, start_http_server, REGISTRY


with open("newdns.yaml", "r") as file:
    dns_services = yaml.safe_load(file)

MONITOR_INTERVAL = 5
DISCOVERY_INTERVAL = 5

def get_dns_status(dns):
    try:
        monitor = dnsmonitor(dns["hostname"], dns["ip_address"], dns["newdns_id"], dns["ip_address"] )
        availability, response_time = monitor.get_status()
        dns["availability"] = availability
        if dns["availability"]:
            dns["loss"] = 0  
            dns["time"] = response_time  
        else:
            dns["loss"] = 100  
            dns["time"] = 0  
    except BaseException as e:
        
        dns["availability"] = False
        dns["loss"] = 100  
        dns["time"] = 0  

    dns_loss.labels(target=dns["ip_address"]).set(dns["loss"])
    dns_time.labels(target=dns["ip_address"]).set(dns["time"])

def main():
    # Start Prometheus server
    start_http_server(8000)
    last_discovery = datetime.now()-timedelta(days=1)
    while True:
        if (datetime.now() - last_discovery).total_seconds() > DISCOVERY_INTERVAL:
            print("Performing DNS discovery")
            last_discovery = datetime.now()
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(get_dns_status, dns_services)
        sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting service-monitor")
        exit()

