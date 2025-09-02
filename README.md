Introduction to to capacity planning and performance analysis with SimPy
========================================================================

This first lab is an introduction to SimPy, a process-based discrete-event simulation framework based on Python. We will see how to use SimPy to simulate simple or complex computer systems and evaluate their performance.

We will simulate a system with multiple parallel servers and a waiting queue, as depicted below.

![Server system](images/system.svg)

We will use SimPy to model this system. This allows us to perform simulations to empirically validate Little's law.

Using SimPy
-----------

### Installation

Follow the tutorial [SimPy in 10 minutes](https://simpy.readthedocs.io/en/latest/simpy_intro/index.html) to install SimPy and run the first examples.

To accelerate the SimPy simulations you can optionally install PyPy, a faster Python interpreter: [PyPy installation](https://doc.pypy.org/en/latest/install.html). If you use PyPy, you need to add the SimPy and NumPy packages to PyPy:

```bash
pypy3 -m ensurepip
pypy3 -m pip install simpy numpy
```

To run simulations with PyPy, use the `pypy3` command instead of `python3`.

Simulation model
----------------

A simulation model for the system shown above is provided in the file `models/little.py`. 

The simulation model has the following structure.

Resource `servers`
:  This SimPy resource represents the servers in the system. It is created with a specified number of parallel servers (`NUM_SERVERS`). Like all SimPy resources, it has a waiting queue where requests wait until one of the servers becomes available.

Function `request_generator`
: This function generates requests at a constant rate. For each request, it creates a new process using the function `process_request`. That process simulates the request processing on the servers.

Function `process_request`
: This function simulates the processing of a request. It adds the request to the waiting queue of the servers, waits for a server to become available, and then simulates the service time. It also records statistics about the service and response times.

Function `record_statistics`
:  This generator function runs periodically to collect statistics about the system, such as the number of requests in the queue.

Main function
:  The main function initializes the simulation environment, creates the server resource then starts the request generator and the statistics recorder. After the simulation it prints the collected statistics.

Exercices
---------

### Understanding the model

Read the code in `models/little.py` and understand how the simulation model works.

### Running the simulation

Run the simulation model with the command:

```bash
python3 models/little.py # Using normal Python
pypy3 models/little.py   # Using PyPy to accelerate the simulation
```

The simulation prints statistics collected during the simulation.

### Compare the results with Little's law

Using Little's law, check if the simulation results correspond to the expected values.

### Modify the simulation

Modify the simulation model to change the parameters of the system, such as the inter-arrival time, service time, and number of servers. Run the simulation again and observe how the results change.
