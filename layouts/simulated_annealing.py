from dash import dcc, html

def create_layout_sa():
    return html.Div([
        html.H1("Simulated Annealing - Network Flow Visualization"),
        
        html.Label("Random Seed:"),
        html.Br(),
        dcc.Input(id="seed-input", type="number", value=5, min=1),
        html.Br(),

        html.Label("Initial Temperature:"),
        html.Br(),
        dcc.Input(id="temp-input", type="number", value=12, min=1, max=100),
        html.Br(),

        html.Label("Cooling Rate:"),
        html.Br(),
        dcc.Input(id="cooling-rate-input", type="number", value=0.2, min=0.01, max=0.99),
        html.Br(),

        html.Button("Run Simulation", id="run-simulation", n_clicks=0),
        dcc.Interval(id='interval', interval=100, n_intervals=0),
        html.Div(id='inflow-output', children=[
            html.P(id="max-inflow-output"),
            html.P(id="temperature-output")
        ]),
        dcc.Graph(id='inflow-graph-dynamic')
    ])
