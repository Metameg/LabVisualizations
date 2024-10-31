import plotly.graph_objects as go
import random

def plot_inflow_over_iterations(sa_instance, initial_temp, cooling_rate, seed):
    random.seed(seed)
    global inflow_data  # Store inflow values for each iteration
    inflow_data = []
    temperature = initial_temp

    # Run simulated annealing and collect inflow values at each iteration
    while temperature > 0.01:
        temperature = temperature*(1-cooling_rate)
        curr_inflow, _, _, temperature = sa_instance.step()  # Run one iteration of SA
        inflow_data.append(curr_inflow)  # Store current inflow
        temperature *= (1 - cooling_rate)  # Update temperature

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(inflow_data))),
        y=inflow_data,
        mode='lines',
        name='Current Inflow'
    ))
    fig.update_layout(
        title="Current Inflow over Iterations",
        xaxis_title="Iteration",
        yaxis_title="Current Inflow"
    )

    return fig, inflow_data