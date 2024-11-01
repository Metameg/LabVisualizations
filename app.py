import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from layouts.simulated_annealing import create_layout_sa
from layouts.additional_tab import additional_tab
from callbacks.simulated_annealing import register_callbacks_sa

app = dash.Dash(__name__)
tabs_styles = {
    'height': '4vh',
    'width': '100%',
    'background': "#323130",
    'border-bottom': '1px solid grey'
}

tab_style = {
    "background": "#323130",
    'text-transform': 'uppercase',
    'color': 'white',
    'border': 'grey',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px'
}

tab_selected_style = {
    "background": "grey",
    'text-transform': 'uppercase',
    'color': 'white',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px'
}

app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='sa', children=[
        dcc.Tab(label='Simulated Annealing', value='sa', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Additional Visualization', value='tab-2', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    

    # Content container with layouts for both tabs, controlled by CSS visibility
    html.Div([
        html.Div(create_layout_sa(), id='sa-content', style={'display': 'block'}),
        html.Div(additional_tab(), id='tab-2-content', style={'display': 'none'})
    ], id='tabs-content-inline', style={'padding': '20px'})
])

register_callbacks_sa(app)
# Toggle visibility based on the active tab
@app.callback(
    [Output('sa-content', 'style'), Output('tab-2-content', 'style')],
    [Input('tabs-styled-with-inline', 'value')]
)
def display_tab_content(selected_tab):
    if selected_tab == 'sa':
        return {'display': 'block'}, {'display': 'none'}
    elif selected_tab == 'tab-2':
        return {'display': 'none'}, {'display': 'block'}


if __name__ == '__main__':
    app.run_server(debug=True)