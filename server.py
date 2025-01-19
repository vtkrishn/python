from flask import Flask
from prometheus_client import start_http_server, Summary, Gauge, Counter, Histogram
import random
import requests
import time
from datetime import datetime
app = Flask(__name__)

request_counter = Counter('app_request_total', 'Total requests to the app')

GC_INCIDENT_STATUS_URL = "https://status.cloud.google.com/incidents.json"

gc_incidents_count = Gauge('gc_incidents_count', 'Number of active incidents')
gc_incidents_gauge = Gauge('gc_incidents', 'GC incidents details', 
                                     ["id", "service_name", "external_desc", "begin", "severity"])

s = Summary('request_latency_seconds', 'Description of summary')
h = Histogram('hist_request_latency_seconds', 'Description of histogram')

@s.time()
@h.time()
def process_summary_requests(t):
    time.sleep(t)

def set_gc_incidents_metrics():
    response = requests.get(GC_INCIDENT_STATUS_URL)
    
    print(response.status_code)
    if response.status_code != 200:
        print("Error: Unable to fetch data from Google Cloud Status API")
        return

    incidents = response.json()

    gc_incidents_count.set(len(incidents))

    # Set incidents details
    for incident in incidents:
        gc_incidents_gauge.labels(
            id=incident.get('id'),
            service_name=incident.get('service_name'),
            external_desc=incident.get('external_desc'),
            begin=incident.get('begin'),
            severity=incident.get('severity')
        ).set(1)


@app.route('/')
def home():
    request_counter.inc()
    curr = datetime.now()
    print(curr)

    import random
    process_summary_requests(random.choice([1,5,10]))

    while True:
        set_gc_incidents_metrics()
        time.sleep(60)

    return str(curr)

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host="0.0.0.0", port=9000)
    
    
