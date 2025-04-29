import dash
import pandas
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Read the SpaceX dataset
spacex_df = pandas.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# create blank figure
def blankfigure():
    figure = go.Figure(go.Scatter(x=[],y=[]))
    figure.update_layout(template = None)
    figure.update_xaxes(showgrid = False, showticklabels = False, zeroline = False)
    figure.update_yaxes(showgrid = False, showticklabels = False, zeroline = False)

    return figure
# Create an app layout
app.layout = html.Div([
    # use bootstrap to create a row with two columns
    dbc.Row([dbc.Col(html.H1("SpaceX Launch Records Dashboard"))]),
                
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dbc.Row([dbc.Col(dcc.Dropdown(id='site-dropdown',
                                options=[{'label': 'ALL', 'value': 'ALL'}] + \
                                        [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True
                                ),
                    )
          ]),
    
    dbc.Row([dbc.Col(dcc.Graph(id='success-pie-chart', figure=blankfigure()))]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    dbc.Row([dbc.Col(dcc.Slider(id='payload-slider',
                                    min=0,
                                    max=spacex_df['Payload Mass (kg)'].max(),
                                    step = None,
                                    marks={},
                                    value=spacex_df['Payload Mass (kg)'].min()), width=3)]),
    dbc.Row([dbc.Col(html.Div(id='slider_value'))]),
    
    # scatter plot
    dbc.Row([dbc.Col(dcc.Graph(id='scatter-chart', figure=blankfigure()))]),
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def pie_chart(site):
    if not site:
        return blankfigure()

    if site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(filtered_df, names='class', title='Total Success Launches for site ' + site)
    return fig

@app.callback(
    Output(component_id='scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
)

def scatter_chart(site, payload):
    if not site:
        return blankfigure()
    
    if site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] <= payload)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == site) & (spacex_df['Payload Mass (kg)'] <= payload)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for site ' + site)
    
    fig.update_traces(marker={'size': 15})
    return fig

@app.callback(
    Output('slider_value', 'children'),
    [Input('payload-slider', 'value')]
)
def update_output(value):
    return f'Selected Value: {value}'

app.run_server(debug=True)