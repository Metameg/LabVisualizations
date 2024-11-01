from dash import dcc, html

def create_layout_sa():
    return html.Div([
        html.H1("Simulated Annealing - Network Flow Visualization"),
        
        html.H2("The Problem"),
        html.P("The objective of the given scenario is to maximize the outflow of a given system. Each edge of the graph has a maximum capacity that can flow through it. There is a starting node S and an exit node E. The goal is to maximize the flow into E.", style= {"margin-bottom": "60px"}),

        html.P("Before Optimization: Flow into E = 2 + 1 + 9 = 12", style={"font-weight": "600", "padding": "20"}),
        html.Img(src='../assets/images/graph_before_optimization.png',style={"width": "100%"}),

        html.P("After Optimization: Flow into E = 2 + 7 + 8 = 17", style={"font-weight": "600", "padding": "20"}),
        html.Img(src='../assets/images/graph_after_optimization.png',style={"width": "100%", "margin-bottom": "60px"}),

        html.H2("Simulation"),

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
        dcc.Graph(id='inflow-graph-dynamic'),

        html.H1("Explanation"),
        html.P("Simulated Annealing is an algorithm used to solve optimization problems efficiently. \
               ")

    ])
