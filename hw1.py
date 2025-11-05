from math import log


# Linear Congruential Generator
class LCG:
    def __init__(self, seed=541, a=29, c=3, m=1289):
        self.seed = seed
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def rand(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m

rng = LCG()

# Distribution helpers
def exponential_var(mean, rng):
    return -log(1 - rng.rand()) * mean

def uniform_var(low, high, rng):
    return low + (high - low) * rng.rand()


def inter_arrival_time(hour, rng):
    times = []
    while sum(times) < hour * 60:
        times.append(round(exponential_var(8, rng), 2))
    return times

def service_time(customer_count, rng):
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
            service.append((round(uniform_var(2, 7, rng), 2), customer_count))
        else:
            service.append((round(uniform_var(2, 4, rng), 2), customer_count))
    return service

inter = inter_arrival_time(.5, rng)
service = service_time(len(inter), rng)
# print(inter)
# print(service_time(len(inter)))

queue = []
events = [(1, 0, "arrival")]
is_service_available = True
output = []

while len(events):
    customer, time, event = events.pop(0)
    time = round(time, 2)
    output.append((customer, time, event))

    if event == "arrival":
        if customer < len(inter):
            events.append((customer+1, time + inter[customer-1], "arrival"))
            
        if is_service_available:
            is_service_available = False
            events.append((customer, time + service[customer-1][0], "departure"))
        else:
            queue.append(customer)

    elif event == "departure":
        is_service_available = True
        if len(queue):
            next_customer = queue.pop(0)
            events.append((next_customer, time + service[next_customer-1][0], "departure"))
            is_service_available = False
    
    events.sort(key=lambda x: (x[1], x[2]))

with open("output.txt", "w") as f:
    f.write(f"Inter-arrival times: {inter}\n")
    f.write(f"Service times: {service}\n\n")
    for customer, time, event in output:
        f.write(f"{customer} {time} {event}\n")


def simulate(rng):
    inter = [0] + inter_arrival_time(8.5, rng)
    service = service_time(len(inter)-1, rng)

    queue = []
    events = [(1, 0, "arrival")]
    is_service_available = True
    output = []

    while len(events):
        customer, time, event = events.pop(0)
        time = round(time, 2)
        output.append((customer, time, event))

        if event == "arrival":
            if customer < len(inter) - 1:
                events.append((customer+1, time + inter[customer-1], "arrival"))
                
            if is_service_available:
                is_service_available = False
                events.append((customer, time + service[customer-1][0], "departure"))
            else:
                queue.append(customer)

        elif event == "departure":
            is_service_available = True
            if len(queue):
                next_customer = queue.pop(0)
                events.append((next_customer, time + service[next_customer-1][0], "departure"))
                is_service_available = False
        
        events.sort(key=lambda x: (x[1], x[2]))

    customers_events = [[-1, -1] for _ in range(len(inter)-1)]
    for customer, time, event in output:
        if event == "arrival":
            customers_events[customer-1][0] = time
        elif event == "departure":
            customers_events[customer-1][1] = time

    customers_data = []
    for customer in range(len(customers_events)):
        customers_data.append(
            {
                "is_lucky": True if customers_events[customer][1] < (8.5 * 60) else False,
                "customer_count": service[customer][1],
                "service_time": service[customer][0],
                "waiting_in_queue": (customers_events[customer][1] - customers_events[customer][0] - service[customer][0]) * service[customer][1],
            }
        )

    lucky_count = sum(customer["customer_count"] if customer["is_lucky"] else 0 for customer in customers_data)
    unlucky_count = sum(data[1] for data in service) - lucky_count

    average_lucky_waiting = sum(customer["waiting_in_queue"] if customer["is_lucky"] else 0 for customer in customers_data) / lucky_count
    if unlucky_count:
        average_unlucky_waiting = sum(customer["waiting_in_queue"] if not customer["is_lucky"] else 0 for customer in customers_data) / unlucky_count
    else:
        average_unlucky_waiting = 0
    
    personnel_utility = sum(customer["service_time"] for customer in customers_data if customer["is_lucky"]) / (8.5 * 60)

    average_ticket_queue_length = sum(customer["waiting_in_queue"]*customer["customer_count"] for customer in customers_data) / (8.5 * 60)

    return lucky_count, unlucky_count, average_lucky_waiting, average_unlucky_waiting, personnel_utility, average_ticket_queue_length


def average_simulation(rng):
    lucky_count, unlucky_count, average_lucky_waiting, average_unlucky_waiting, personnel_utility, average_ticket_queue_length = 0, 0, 0, 0, 0, 0
    for _ in range(7):
        l, u, a, b, c, d = simulate(rng)
        lucky_count += l
        unlucky_count += u
        average_lucky_waiting += a
        average_unlucky_waiting += b
        personnel_utility += c
        average_ticket_queue_length += d

    with open(f"7_day_{rng.seed}.txt", "w") as f:
        f.write(f"Lucky count: {round(lucky_count, 2)} customers\n")
        f.write(f"Unlucky count: {round(unlucky_count, 2)} customers\n")
        f.write(f"Average lucky waiting: {round(average_lucky_waiting / 7, 2)} minutes\n")
        f.write(f"Average unlucky waiting: {round(average_unlucky_waiting / 7, 2)} minutes\n")
        f.write(f"Personnel utility: {round(personnel_utility / 7, 2)} customers\n")
        f.write(f"Average ticket queue length: {round(average_ticket_queue_length / 7, 2)} customers\n")

average_simulation(LCG(seed=542))
average_simulation(LCG(seed=543))
average_simulation(LCG(seed=544))
average_simulation(LCG(seed=545))


