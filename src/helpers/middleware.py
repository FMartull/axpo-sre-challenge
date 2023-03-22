from flask import request
import time
import sys

from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('test_app', request.path).observe(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels('test_app', request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(bucket_blueprint):
    bucket_blueprint.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    bucket_blueprint.after_request(record_request_data)
    bucket_blueprint.after_request(stop_timer)