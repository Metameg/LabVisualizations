import dash
from dash import dcc, html, callback_context
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import networkx as nx
from SA import SA
from collections import deque
import random
import plotly.graph_objects as go

# Instantiate your Simulated Annealing class with a sample graph
G = nx.DiGraph()
G.add_edges_from([(0, 1, {'flow': 5}), (0, 1,{'capacity': 10}),
 (0, 2,{'flow': 3}), (0, 2,{'capacity': 8}),
  (0,3,{'flow': 4}), (0,3,{'capacity': 11}),
   (1,2, {'flow': 3}), (1,2,{'capacity': 9}),
    (1,5, {'flow': 2}), (1,5,{'capacity': 3}),              # modified from last sversion: edge (1,4) replaced by edge (1,5)
     (2,4, {'flow': 7}), (2,4,{'capacity': 9}),
      (2,5, {'flow': 1}), (2,5,{'capacity': 8}),
       (3,2, {'flow': 2}), (3,2,{'capacity': 8}),
        (3,4,{'flow': 2}), (3,4,{'capacity': 12}),
         (4,5, {'flow': 9}), (4,5,{'capacity': 9})])
# Sample graph initialization here

INIT_T = 12
INIT_A = 0.2
SEED = 5

sa_static = SA(G, INIT_T, INIT_A)
sa_dynamic = SA(G, INIT_T, INIT_A)  # Initialize the simulated annealing class with your graph

app = dash.Dash(__name__)

# Variables to track temperature and inflow over time
inflow_data = []  # Initial inflow



def plot_inflow_over_iterations(sa_instance, initial_temp, cooling_rate):
    random.seed(SEED)
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

# Initial setup for the static background inflow figure
static_fig, inflow_data = plot_inflow_over_iterations(sa_static, INIT_T, INIT_A)
dynamic_fig = go.Figure(static_fig)
# Dash Layout
app.layout = html.Div([
    html.H1("Simulated Annealing - Network Flow Visualization"),
    # Input fields for SEED, INIT_T, and INIT_A
    html.Label("Random Seed:"),
    dcc.Input(id="seed-input", type="number", value=SEED),  # Default value is SEED
    html.Br(),
    
    html.Label("Initial Temperature:"),
    dcc.Input(id="temp-input", type="number", value=INIT_T, min=1, max=100),  # Default value is INIT_T
    html.Br(),
    
    html.Label("Cooling Rate:"),
    dcc.Input(id="cooling-rate-input", type="number", value=INIT_A, min=0.01, max=0.99, step=0.01),  # Default value is INIT_A
    html.Br(),
    html.Button("Run Simulation", id="run-simulation", n_clicks=0),

    dcc.Interval(id='interval', interval=100, n_intervals=0),  
    html.Div(id='inflow-output', children=[
        html.P(id="max-inflow-output"),
        html.P(id="temperature-output")
    ]),
    dcc.Graph(id='inflow-graph-dynamic') 
])

last_n_clicks = 0
# Callback to update graph and inflow values
@app.callback(
    [
        Output('max-inflow-output', 'children'),
        Output('temperature-output', 'children'), 
        Output('inflow-graph-dynamic', 'figure'), 
        Output('interval', 'disabled'),  
        Output('temp-input', 'disabled'), 
        Output('cooling-rate-input', 'disabled'),  
        Output('seed-input', 'disabled')
    ],
    [
        Input('interval', 'n_intervals'),
        Input("run-simulation", "n_clicks"),
        Input("seed-input", "value"),
        Input("temp-input", "value"),
        Input("cooling-rate-input", "value")
    ],
    prevent_initial_call=True  # Prevent callback from being called on initial load
)
def update_simulation(n_intervals, n_clicks, seed_value, temp_value, cooling_rate_value):
    global inflow_data, dynamic_fig, static_fig, sa_dynamic, last_n_clicks, SEED, INIT_T, INIT_A

    # Update global variables with new input values
    SEED = seed_value
    INIT_T = temp_value
    INIT_A = cooling_rate_value

    if n_clicks is None or n_clicks == 0:
        return (dash.no_update, 
                dash.no_update, 
                dash.no_update, 
                dash.no_update, 
                False, False, False)

     # Validate temperature and cooling rate
    if temp_value < 1:
        return ("Error: Temperature must be greater than or equal to 1", 
                dash.no_update, 
                dash.no_update, 
                dash.no_update, 
                False, False, False)
    if cooling_rate_value < 0.01:
        return ("Error: Cooling rate must be greater than or equal to 0.01", 
                dash.no_update, 
                dash.no_update, 
                dash.no_update, 
                False, False, False)

    # Determine which input triggered the callback
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    # If seed, temp, or cooling rate changes, update static and dynamic backgrounds
    if triggered_id in {"seed-input", "temp-input", "cooling-rate-input"}:
        random.seed(SEED)
        sa_static = SA(G, INIT_T, INIT_A)
        static_fig, _ = plot_inflow_over_iterations(sa_static,INIT_T, INIT_A)
        
        # Set dynamic_fig to be static_fig initially
        dynamic_fig = go.Figure(static_fig)
        
        return  (dash.no_update, 
                dash.no_update, 
                dynamic_fig, 
                dash.no_update, 
                False, False, False)
    
    # Reset the simulation if the button is clicked again after completion
    if n_clicks != last_n_clicks:
        random.seed(SEED)
        last_n_clicks = n_clicks
        sa_dynamic = SA(G, INIT_T, INIT_A)   # Reset the simulated annealing object
        # Reset the intervals
        n_intervals = 0 

    # Run a single step of simulated annealing
    _, max_inflow, _, temperature = sa_dynamic.step()

    # Check if the simulation is complete
    if temperature < 0.01:
        return (f"Simulation Complete. Max Inflow: {max_inflow:.2f}", 
                "Temperature: 0", 
                dynamic_fig, 
                True, 
                False, 
                False, 
                False)
    
    # Clear previous Max Inflow trace
    dynamic_fig.data = [trace for trace in dynamic_fig.data if trace.name != "Max Inflow"]

    # Add new max_inflow trace
    dynamic_fig.add_trace(go.Scatter(
        x=list(range(len(inflow_data))),  
        y=[max_inflow] * len(inflow_data),  
        mode='lines',
        name='Max Inflow',
        line=dict(dash='dash', color='red')
    ))

    return (f"Max Inflow: {max_inflow:.2f}", 
            f"Current Temperature: {temperature:.2f}", 
            dynamic_fig, 
            False, 
            True, 
            True, 
            True)

if __name__ == '__main__':
    app.run_server(debug=True)
