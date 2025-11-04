# Configuration for the cinema simulation

SHOW_CAPACITY = 250
MEAN_INTERARRIVAL = 8.0
START_TIME = 10 * 60
SHOW_TIME = 18 * 60 + 30
TICKET_OPTIONS = (1, 2, 3, 4)
TICKET_PROB = (0.30, 0.40, 0.20, 0.10)
PAYMENT_OPTIONS = (
    ("cash", 0.25, (2.0, 7.0)),
    ("card", 0.75, (2.0, 4.0)),
)
TEST_WINDOW_MINUTES = 30
REPLICATIONS = 4
DAYS_PER_REPLICATION = 7


# Linear Congruential Generator
class LCG:
    def __init__(self, seed=541, a=29, c=3, m=1289):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def rand(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m


import math
import heapq
from collections import deque

rng = LCG()

# Distribution helpers
def exponential_var(mean):
    return -math.log(1 - rng.rand()) * mean

def uniform_var(low, high):
    return low + (high - low) * rng.rand()


def inter_arrival_time(hour):
    times = []
    while sum(times) < hour * 60:
        times.append(round(exponential_var(MEAN_INTERARRIVAL), 2))
    return times

def 

print(inter_arrival_time(1))

def sample_payment(rng):
    u = rng.rand()
    cumulative = 0.0
    for method, prob, bounds in PAYMENT_OPTIONS:
        cumulative += prob
        if u <= cumulative:
            service_time = uniform_var(bounds[0], bounds[1], rng)
            return method, service_time
    method, _, bounds = PAYMENT_OPTIONS[-1]
    return method, uniform_var(bounds[0], bounds[1], rng)

