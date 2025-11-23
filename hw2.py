import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
e = 2.718281828459045

def poisson_var(lambda_param, rng):
    limit = e**(-lambda_param)
    p = rng.rand()
    n = 0
    while p > limit:
        p *= rng.rand()
        n += 1
    return n


def simulate_day(rng):
    """
    Generate hourly customer arrivals for a nonstationary Poisson process.
    
    Parameters:
    num_days (int): Number of days to simulate
    
    Returns:
    list: List of tuples (datetime, hour_index, arrivals) for each hour
    """
    # Define arrival rates by time interval (customers per hour)
    arrival_rates = {
        (10, 12): 19,  # 10 am to 12 pm
        (12, 14): 25,  # 12 pm to 2 pm
        (14, 16): 27,  # 2 pm to 4 pm
        (16, 20): 42,  # 4 pm to 8 pm
        (20, 22): 25   # 8 pm to 10 pm
    }
    
    results = []
    
    for hour in range(24):
        # hour represents the interval between (hour, hour+1)
        if 10 <= hour < 12:
            rate = arrival_rates[(10, 12)]
        elif 12 <= hour < 14:
            rate = arrival_rates[(12, 14)]
        elif 14 <= hour < 16:
            rate = arrival_rates[(14, 16)]
        elif 16 <= hour < 20:
            rate = arrival_rates[(16, 20)]
        elif 20 <= hour < 22:
            rate = arrival_rates[(20, 22)]
        else:
            rate = 0
        
        arrivals = poisson_var(rate, rng)
        results.append((hour, arrivals))
    
    return results


num_days = 4
results = [simulate_day(rng) for _ in range(num_days)]

all_hours = []
all_arrivals = []
day_labels = []

hour_index = 0
for day_idx, day_results in enumerate(results):
    for hour, arrivals in day_results:
        all_hours.append(hour_index)
        all_arrivals.append(arrivals)
        day_labels.append(f"Day {day_idx + 1}, {hour:02d}:00")
        hour_index += 1

# Plotly figure oluştur
fig = go.Figure()

# Ana çizgi grafiği
fig.add_trace(go.Scatter(
    x=all_hours,
    y=all_arrivals,
    mode='lines+markers',
    name='Hourly Arrivals',
    line=dict(color='#1f77b4', width=2),
    marker=dict(size=4, color='#1f77b4'),
    hovertemplate='<b>%{text}</b><br>' +
                    'Arrivals: %{y}<br>' +
                    'Hour Index: %{x}<extra></extra>',
    text=day_labels
))

for day in range(1, num_days):
    x_position = day * 24 - 0.5
    fig.add_vline(
        x=x_position,
        line_dash="dash",
        line_color="gray",
        opacity=0.5,
        annotation_text=f"Day {day + 1}",
        annotation_position="top"
    )

fig.update_layout(
    title={
        'text': f'Hourly Customer Arrivals Over {num_days} Days',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20}
    },
    xaxis_title='Hour Index',
    yaxis_title='Number of Arrivals',
    hovermode='closest',
    template='plotly_white',
    width=1200,
    height=600,
    showlegend=True
)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

fig.write_html('hourly_arrivals_4days_plotly.html')
print(f"\nPlotly görselleştirmesi 'hourly_arrivals_4days_plotly.html' dosyasına kaydedildi")

fig.show()



num_days = 7
results = [simulate_day(rng) for _ in range(num_days)]

total_between_2_4_pm = 0
for day_results in results:
    for hour, arrivals in day_results:
        if 14 <= hour < 16:
            total_between_2_4_pm += arrivals

print(f"Average arrivals (lambda) between 2 and 4 pm: {total_between_2_4_pm / num_days / 2}")



