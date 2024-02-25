from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import threading
import sys


class WorkerManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.workers = []
        return cls._instance

    def add_worker(self, worker_url):
        self.workers.append(worker_url)

    def get_next_worker_url(self):
        if not self.workers:
            raise ValueError("No workers available")
        return self.workers.pop(0)


# Currently the server handles only get requests
class LoadBalancer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.worker_manager = kwargs.pop('worker_manager')
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_url = urlparse(self.path)

        # Get the next worker using round robin
        worker_url = self.worker_manager.get_next_worker_url()
        self.worker_manager.add_worker(worker_url)

        # Create the full URL including query parameters if existing
        full_url = f"{worker_url}{parsed_url.path}"
        if parsed_url.query:
            full_url += "?" + parsed_url.query

        self.send_response(302)
        self.send_header('Location', full_url)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


def start_load_balancer(host, port, worker_manager):
    print("Start balancing the requests for workers: " + ', '.join(worker_manager.workers))
    server = HTTPServer((host, port),
                        lambda *args, **kwargs: LoadBalancer(*args, **kwargs, worker_manager=worker_manager))
    server.serve_forever()


if __name__ == "__main__":
    # Get the list of worker URLs from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python load_balancer.py <worker_url_1> <worker_url_2> ...")
        sys.exit(1)
    worker_urls = sys.argv[1:]

    # Create a WorkerManager instance and add workers to it
    worker_manager = WorkerManager()
    for worker_url in worker_urls:
        worker_manager.add_worker(worker_url)

    load_balancer_host = '127.0.0.1'
    load_balancer_port = 8000
    start_load_balancer(load_balancer_host, load_balancer_port, worker_manager)
