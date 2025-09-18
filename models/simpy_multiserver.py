"""SimPy simulation model of an multiserver system with a queue.
  - The request_generator function generates requests with a uniformly distributed inter-arrival time.
  - The servers are un SimPy resource with capacity equal to the number of servers.
  - The process_request function simulates the processing of each request, using a constant service time.
"""

from numpy.random import uniform
import simpy

# ---------------------------------------------------------------------------
# SimPy model

class MultiServer:
    """Class representing a multi-server queueing system using SimPy."""

    def __init__(self, env, num_servers, interarrival_time, service_time):
        """Initialize the parameters of the multi-server queueing system and the statistics arrays."""
        self.env = env
        self.servers = simpy.Resource(env, capacity=num_servers)
        self.interarrival_time = interarrival_time
        self.service_time = service_time

        # Result statistics
        self.interarrival_times = [] # List to store inter-arrival times of requests
        self.queueing_times = [] # List to store queueing times of each request
        self.queue_lengths = []  # List to store the length of the queue at each request
        self.service_times = []  # List to store service times of each request
        self.busy_servers = []   # List to store the number of busy servers at each request
        self.response_times = [] # List to store response times of each request
        self.users_in_system = [] # List to store the number of users in the system at each request


    def request_generator(self):
        """Generate requests with a uniformly distributed inter-arrival time."""
        while True:
            interarrival = uniform(0, self.interarrival_time * 2)
            self.interarrival_times.append(interarrival)
            yield self.env.timeout(interarrival)
            self.env.process(self.process_request())


    def process_request(self):
        """Place a request in the queue, then process it when a server is available.
        
        The method also records statistics about the service, response, and queueing times.
        """
        # Place the request in the queue
        arrival_time = self.env.now
        job = self.servers.request()
        # Wait for the server to become available (wait in the queue)
        yield job
        service_start_time = self.env.now
        # Process the request
        yield self.env.timeout(uniform(0, self.service_time * 2))
        # Release the server
        self.servers.release(job)

        # Record delay statistics
        self.service_times.append(self.env.now - service_start_time)
        self.response_times.append(self.env.now - arrival_time)
        self.queueing_times.append(service_start_time - arrival_time)


    def record_statistics(self, sampling_interval):
        """Periodically collect statistics about the number of tasks in the system.

        Remark for advanced users: we cannot record the statistics in the function
        process_request, because only Poisson arrivals see time averages (PASTA).
        """
        while True:
            yield self.env.timeout(sampling_interval)
            self.queue_lengths.append(len(self.servers.queue))
            self.busy_servers.append(self.servers.count)
            self.users_in_system.append(self.servers.count + len(self.servers.queue))
