"""SimPy simulation of an multiserver system with a queue.
  - The request_generator function generates requests with a uniformly distributed inter-arrival time.
  - The servers are un SimPy resource with capacity equal to the number of servers.
  - The process_request function simulates the processing of each request, using a constant service time.
"""

import random
from numpy import mean
import simpy

# Parameters -- change these to adjust the simulation
INTERARRIVAL_TIME = 1.0    # Average time between requests
SERVICE_TIME = 4.0         # Average service time for each request
NUM_SERVERS = 5            # Number of parallel servers in the system
SIM_DURATION = 1_000_000.0 # Total time for the simulation
SAMPLING_INTERVAL = 1.0    # Interval for collecting statistics

# Result statistics
interarrival_times = [] # List to store inter-arrival times of requests
queueing_times = [] # List to store queueing times of each request
queue_lengths = []  # List to store the length of the queue at each request
service_times = []  # List to store service times of each request
busy_servers = []   # List to store the number of busy servers at each request
response_times = [] # List to store response times of each request
users_in_system = [] # List to store the number of users in the system at each request

# ---------------------------------------------------------------------------
# SimPy model

def request_generator(env, servers):
    """Generate requests with a uniformly distributed inter-arrival time."""
    while True:
        interarrival = random.uniform(0, INTERARRIVAL_TIME * 2)
        interarrival_times.append(interarrival)
        yield env.timeout(interarrival)
        # Schedule the processing of the request at time NOW.
        # Since we do not use yield, this will NOT wait for the process to finish.
        env.process(process_request(env, servers))


def process_request(env, servers):
    """Place a request in the queue, then process it when a server is available.
    
    The function also records statistics about the service, response, and queueing times.
    """
    # Place the request in the queue
    arrival_time = env.now
    job = servers.request()
    # Wait for the server to become available (wait in the queue)
    yield job
    service_start_time = env.now
    # Process the request
    yield env.timeout(random.uniform(0, SERVICE_TIME * 2))
    # Release the server
    servers.release(job)

    # Record delay statistics
    service_times.append(env.now - service_start_time)
    response_times.append(env.now - arrival_time)
    queueing_times.append(service_start_time - arrival_time)


def record_statistics(env, servers):
    """Periodically collect statistics about number of task in the system.

    Remark for advanced users: we cannot record the statistics in the function
    process_request, because only Poisson arrivals see time averages (PASTA).
    """
    while True:
        yield env.timeout(SAMPLING_INTERVAL)
        queue_lengths.append(len(servers.queue))
        busy_servers.append(servers.count)
        users_in_system.append(servers.count + len(servers.queue))


# ---------------------------------------------------------------------------
def main():
    """Run the simulation and print statistics."""

    # Create the simulation environment and the server resource
    env = simpy.Environment()
    servers = simpy.Resource(env, capacity=NUM_SERVERS)
    env.process(request_generator(env, servers))
    env.process(record_statistics(env, servers))

    # Run the simulation
    env.run(until=SIM_DURATION)

    # Compute and print the results
    print("---- Queueing system -----")
    print(f'Mean queue length: {mean(queue_lengths):.4f}')
    print(f'Arrival rate: {1.0/mean(interarrival_times):.4f}')
    print(f'Mean queueing time: {mean(queueing_times):.4f} s')
    print("---- Server system -----")
    print(f'Mean busy servers: {mean(busy_servers):.4f}')
    print(f'Arrival rate: {1.0/mean(interarrival_times):.4f}')
    print(f'Mean service time: {mean(service_times):.4f}')
    print("---- Complete system -----")
    print(f'Mean users in system: {mean(users_in_system):.4f} s')
    print(f'Arrival rate: {1.0/mean(interarrival_times):.4f}')
    print(f'Mean response time: {mean(response_times):.4f} s')

if __name__ == '__main__':
    main()
