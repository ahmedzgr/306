from math import log

SHOW_CAPACITY = 250
MEAN_INTERARRIVAL = 8.0
START_TIME = 10 * 60
SHOW_TIME = 18 * 60 + 30
TICKET_OPTIONS = (1, 2, 3, 4)
TICKET_PROB = (0.30, 0.40, 0.20, 0.10)
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

rng = LCG(seed=541)

# Distribution helpers
def exponential_var(mean):
    return -log(1 - rng.rand()) * mean

def uniform_var(low, high):
    return low + (high - low) * rng.rand()


def inter_arrival_time(hour):
    times = []
    while sum(times) < hour * 60:
        times.append(round(exponential_var(MEAN_INTERARRIVAL), 2))
    return times

def service_time(customer_count):
    service = []
    for _ in range(customer_count):
        r = rng.rand()
        if r < 0.3:
            customer_count = 1
        elif r < 0.7:
            customer_count = 2
        elif r < 0.9:
            customer_count = 3
        else:
            customer_count = 4

        if rng.rand() < 0.25:
            service.append((round(uniform_var(2, 7), 2), customer_count))
        else:
            service.append((round(uniform_var(2, 4), 2), customer_count))
    return service

inter = inter_arrival_time(.5)
service = service_time(len(inter))
print(inter)
print(service_time(len(inter)))

inter.pop()
queue = []
events = [(1, 0, "arrival")]
is_service_available = True
final_events = []

while len(events):
    customer, time, event = events.pop(0)
    time = round(time, 2)
    final_events.append((customer, time, event))
    if event == "arrival":
        if customer < len(inter):
            events.append((customer+1, time + inter[customer], "arrival"))
        if is_service_available:
            final_events.append((customer, time, "service_start"))
            is_service_available = False
            events.append((customer, time + service[customer][0], "departure"))
        else:
            queue.append(customer)
            
    elif event == "service_start":
        is_service_available = False
        events.append((customer, time + service[customer][0], "departure"))

    elif event == "departure":
        is_service_available = True
        if len(queue):
            events.append((queue.pop(0), time, "service_start"))
            is_service_available = False
    else:
        raise ValueError(f"Invalid event: {event}")
    events.sort(key=lambda x: x[1])

with open("output.txt", "w") as f:
    f.write(f"Inter-arrival times: {inter}\n")
    f.write(f"Service times: {service}\n")
    for customer, time, event in final_events:
        f.write(f"{customer} {time} {event}\n")