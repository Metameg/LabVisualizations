from dash import dcc, html

def create_layout_sa():
    return html.Div([
        html.H1("Simulated Annealing - Network Flow Visualization"),
        
        html.H2("The Problem"),
        html.P("The objective of the given scenario is to maximize the outflow of a given system. Each edge of the graph has a maximum capacity that can flow through it. There is a starting node S and an exit node E. The goal is to maximize the flow into E."),

        html.P("Note: Conservation of flow at each node must be conserved.", style={"font-weight": "600"}),
        html.P("That is, the flow into must always be equal to the flow out of each node.", style= {"margin-bottom": "60px"}),

        html.P("Before Optimization: Flow into E = 2 + 1 + 9 = 12", style={"font-weight": "600", "padding": "20"}),
        html.Img(src='../assets/images/graph_before_optimization.png',style={}),

        html.P("After Optimization: Flow into E = 2 + 7 + 8 = 17", style={"font-weight": "600", "padding": "20"}),
        html.Img(src='../assets/images/graph_after_optimization.png',style={"margin-bottom": "60px"}),

        html.H2("Simulation"),

        html.H3("Directions"),

        html.P("1. Input a seed value for randomization to ensure reproducibility of results. This seed will control the random generation of the flow at each iteration plot."),

        html.P("2. Choose an initial temperature and a cooling rate (a value between 0 and 1 to control how quickly the temperature decreases)."),

        html.P("3. Run the Simulation. The goal is to have the max-inflow (represented by the red line) of the simulation converge to the global maximum of the generated plot. A low cooling rate may increase the likelihood of this convergence at the cost of time to run the simulation due to the increased number of iterations in the algorithm."),

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
        dcc.Input(id="cooling-rate-input", type="number", value=0.2, min=0.01, max=0.99, step=0.01),
        html.Br(),

        html.Button("Run Simulation", id="run-simulation", n_clicks=0),
        dcc.Interval(id='interval', interval=100, n_intervals=0),
        html.Div(id='inflow-output', children=[
            html.P(id="max-inflow-output"),
            html.P(id="temperature-output")
        ]),
        dcc.Graph(id='inflow-graph-dynamic'),

        html.H1("Explanation"),
        html.P("Simulated annealing (SA) is a probabilistic optimization technique inspired by the annealing process in metallurgy, where materials are heated and then slowly cooled to reach a stable, low-energy state."),

        html.P("In SA, we start with an initial solution and iteratively explore neighboring solutions by making small random changes. Each new solution is evaluated with an objective function, which determines its energy. If the new solution is better (lower energy), it is accepted; if worse, it may still be accepted with a certain probability that decreases over time."),

        html.P("This acceptance of less favorable solutions allows the algorithm to escape local optima early on, while the gradual reduction in probability, controlled by a cooling schedule, refines the search as it progresses. Over many iterations, the system cool and converges towards a near-optimal solution.")

    ])
