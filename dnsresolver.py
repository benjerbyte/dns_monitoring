import time
from dns.resolver import Resolver, Timeout, NXDOMAIN

from prometheus_client import Gauge

dns_loss = Gauge('dns_packet_loss', 'DNS Packet Loss Percentage', ['target'])
dns_time = Gauge('dns_response_time', 'DNS PTT in milliseconds', ['target'])

class servicemonitor:
    def __init__(self, hostname, ip_address, newdns_id,target,data=None):
        self.hostname= hostname
        self.ip_address= ip_address
        self.newdns_id= newdns_id
        self.target= target
        self.data = data

    def get_status(self):
        pass
    
class dnsmonitor(servicemonitor):
    def get_status(self):
        target_resolver = Resolver()
        target_resolver.nameservers = [self.ip_address]  
        loss = 0.0 
        time_start = time.time()
        try:
            response = target_resolver.query(self.hostname)
            if  ( response is not None and response.response is not None and len(response.response.answer) > 0 ):
                t = time.time() - time_start
                dns_time.labels(self.ip_address).set(t)
                dns_loss.labels(self.ip_address).set(loss)
                return True, t
        except NXDOMAIN as loss:
            loss = 100.0
        except Timeout as loss:
            loss = 100.0
        except BaseException as loss:
            loss = 100.0

        dns_time.labels(self.ip_address).set(0.0)
        dns_loss.labels(self.ip_address).set(loss)
        return False, 0.0

                     
