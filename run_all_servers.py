import subprocess
import time
import sys
import signal

# Global list to store subprocesses
subprocesses = []


def start_load_balancer(host, port, worker_urls):
    print(f"Starting load balancer on {host}:{port}...")
    process = subprocess.Popen(["python", "load_balancer.py"] + worker_urls)
    subprocesses.append(process)


def start_worker(host, port):
    print(f"Starting Django worker on port {port}...")
    process = subprocess.Popen(["python", "manage.py", "runserver", f"{host}:{port}"])
    subprocesses.append(process)


def graceful_exit(signum, frame):
    print("\nGracefully exiting...")
    for process in subprocesses:
        process.terminate()
    sys.exit(0)


if __name__ == "__main__":
    # Register the signal handler for graceful exit
    signal.signal(signal.SIGINT, graceful_exit)

    # Get the number of workers from command line argument
    if len(sys.argv) < 2:
        print("Usage: python run_all_servers.py <number_of_workers>")
        sys.exit(1)
    try:
        num_workers = int(sys.argv[1])
    except ValueError:
        print("Invalid number of workers. Please provide an integer.")
        sys.exit(1)

    # Start the load balancer
    host = "localhost"
    load_balancer_port = 8000
    worker_urls = [f"http://localhost:800{i + 1}" for i in range(num_workers)]
    start_load_balancer(host, load_balancer_port, worker_urls)

    # Wait for a short time for the load balancer to start
    time.sleep(2)

    # Start Django worker servers
    for i in range(num_workers):
        port = 8001 + i  # Start worker servers from port 8001 onwards
        start_worker(host, port)

    while True:
        time.sleep(1)
