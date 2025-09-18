
from numpy import mean
import simpy
from models.simpy_multiserver import MultiServer

# Parameters -- change these to adjust the simulation
INTERARRIVAL_TIME = 1.0    # Average time between requests
SERVICE_TIME = 4.0         # Average service time for each request
NUM_SERVERS = 5            # Number of parallel servers in the system
SIM_DURATION = 1_000_000.0 # Total time for the simulation
SAMPLING_INTERVAL = 1.0    # Interval for collecting statistics

# ---------------------------------------------------------------------------
# Main function to run simulation model

def main():
    """Run the simulation and print statistics."""

    # Create the simulation environment and the server resource
    env = simpy.Environment()
    model = MultiServer(env, NUM_SERVERS, INTERARRIVAL_TIME, SERVICE_TIME)

    # Start the request generator and the statistics recorder

    env.process(model.request_generator())
    env.process(model.record_statistics(SAMPLING_INTERVAL))

    # Run the simulation
    env.run(until=SIM_DURATION)

    # Compute and print the results
    print("---- Queueing system -----")
    print(f'Mean queue length: {mean(model.queue_lengths):.4f}')
    print(f'Arrival rate: {1.0/mean(model.interarrival_times):.4f}')
    print(f'Mean queueing time: {mean(model.queueing_times):.4f} s')
    print("---- Server system -----")
    print(f'Mean busy servers: {mean(model.busy_servers):.4f}')
    print(f'Arrival rate: {1.0/mean(model.interarrival_times):.4f}')
    print(f'Mean service time: {mean(model.service_times):.4f}')
    print("---- Complete system -----")
    print(f'Mean users in system: {mean(model.users_in_system):.4f} s')
    print(f'Arrival rate: {1.0/mean(model.interarrival_times):.4f}')
    print(f'Mean response time: {mean(model.response_times):.4f} s')

if __name__ == '__main__':
    main()
