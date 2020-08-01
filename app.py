import os
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import plotly.express as px

import numpy as np
import pandas as pd

hurricane_count = pd.read_csv('data/hur_data.csv')

hurricane_energy = pd.read_csv('data/cyclone_energy.csv')

continent_temp = pd.read_csv('data/revised_cont.csv')

global_temp_data = pd.read_csv('data/qtemp.csv')

arctic_ice = pd.read_csv('data/arctic_sea_ice.csv', sep = '\t')

sea_levels = pd.read_csv('data/sea_levels.csv')
sea_levels['Adjusted Sea Levels (mm)'] = 25.4*sea_levels['CSIRO - Adjusted sea level (inches)']


##### static graphs###############################################################
### continent_animation #################################################
###############################################################################

temperature_animation = px.bar(continent_temp, x = 'Region', y = 'Temp', animation_frame = 'Year', color = 'Region',
opacity = .8, range_y = [6, 24] )

temperature_animation.update_layout(
    title = "Temperature On Populated Continents Over the Years",
    yaxis = dict(
        title = 'Temperature °C'
    )

)

global_temp_map = px.choropleth(global_temp_data, locations = 'Country', color = 'Average Temperature', locationmode = 'country names', animation_frame = 'Date', color_continuous_scale="rdbu_r", range_color = (-4, 35),  labels={'Average Temperature':'Average Temperature (°C)'}

)

global_temp_map.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    autosize = True,
)

arctic_ice_graph = go.Figure()
arctic_ice_graph.add_trace(
    go.Scatter(
        x = arctic_ice.year,
        y = arctic_ice[' extent'],
        name = 'Ice Extent'
    )
)

arctic_ice_graph.add_trace(
    go.Scatter(
        x = arctic_ice.year,
        y = arctic_ice['   area'],
        name = "Ice Area"
    )
)

arctic_ice_graph.update_layout(
    title = 'Arctic Ice Levels',
    xaxis = dict(
        title = 'Years'
    ),
    yaxis = dict(
        title = 'km of Ice for extent, km squared for area'
    ),
    showlegend = False
)

sea_levels_graph = go.Figure(go.Scatter(
    x = sea_levels.Year,
    y = sea_levels['Adjusted Sea Levels (mm)']
))

sea_levels_graph.update_layout(
    title = "Sea Levels vs Year",
    xaxis = dict(
        title = 'Year'
    ),
    yaxis = dict(
        title = 'Rise in Sea Levels (mm)'
    ),
)

#########################################
######## Plotly layout starts###################
##########################################3

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = html.Div([
    html.Div([
        html.P("Global Temperature, Hurricanes, Ocean levels and Arctic Sea Ice Levels", style = {
            'font-size':'25px',
            'font-weight':'bold',
            'font-family':'Verdana',
            'padding-left':'20px',
            'color':'lightblue'
        })
    ], style = {
        'width':'100%',
        'float':'left',
    }),
    html.Div([
        dcc.Graph(figure = global_temp_map,
            style = {
                'width':'58%',
                'float':'left',
                'padding':'20px',
            })
    ]),
    html.Div([
        dcc.Graph(
            figure = arctic_ice_graph
        )
    ], style = {
        'width':'34%',
        'float':'left',
        'padding':'20px'
    }),

    html.Div([
        dcc.Graph(
            figure = sea_levels_graph
        )
    ], style = {
        'width':'20%',
        'float':'left',
        'padding':'20px'
    }),
    html.Div([
        dcc.Graph(figure = temperature_animation)
    ], style = {
        'width':'45%',
        'float':'left',
        'padding':'20px'
    }),
    html.Div([
        html.Button('Number of Hurricanes', id='hur_num', n_clicks=0, style = {
            'width':'50%',
            'height':'30px'
        }),
        html.Button('Cyclone Energy', id='hur_energy', n_clicks=0, style = {
            'width':'50%',
            'height':'30px'
        }),
        html.Div(id = 'hurricane_container')
        ], style = {
            'width':'25%',
            'float':'left',
            'padding':'20px',
        }),

])



### callbacks start here
@app.callback(
    Output('hurricane_container', 'children'),
    [Input('hur_num', 'n_clicks'),
    Input('hur_energy', 'n_clicks')]
)

def display_hurricane_data(number, energy):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'hur_num' in changed_id:
        hurricane_graph = go.Figure()
        hurricane_graph.add_trace(go.Scatter(
            x = hurricane_count.Year,
            y = hurricane_count['Total hurricanes (adjusted)'],
            name = 'Adjusted for Technology Limitations'
        ))
        hurricane_graph.add_trace(go.Scatter(
            x = hurricane_count.Year,
            y = hurricane_count['Total hurricanes (unadjusted)'],
            name = 'Unadjusted'
        ))
        hurricane_graph.update_layout(
            title = 'Hurricane Count vs Year',
            xaxis = dict(
                title = 'Year'
            ),
            yaxis = dict(
                title = 'Hurricane Count'
            ),
            showlegend = False
        )
        msg = dcc.Graph(figure = hurricane_graph)
    elif 'hur_energy' in changed_id:
        hurricane_graph = go.Figure(go.Scatter(
            x = hurricane_energy.Year,
            y = hurricane_energy.ACE,
        ))
        hurricane_graph.update_layout(
            title = 'Acculated Cyclone Energy vs Year',
            xaxis = dict(
                title = 'Year'
            ),
            yaxis = dict(
                title = 'Accumulated Cyclone Energy Index'
            ),
        )
        msg = dcc.Graph(figure = hurricane_graph)

    else:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'hur_num' in changed_id:
            hurricane_graph = go.Figure()
            hurricane_graph.add_trace(go.Scatter(
                x = hurricane_count.Year,
                y = hurricane_count['Total hurricanes (adjusted)'],
                name = 'Adjusted for Technology Limitations'
            ))
            hurricane_graph.add_trace(go.Scatter(
                x = hurricane_count.Year,
                y = hurricane_count['Total hurricanes (unadjusted)'],
                name = 'Unadjusted'
            ))
            hurricane_graph.update_layout(
                title = 'Hurricane Count vs Year',
                xaxis = dict(
                    title = 'Year'
                ),
                yaxis = dict(
                    title = 'Hurricane Count'
                ),
                showlegend = False
            )
            msg = dcc.Graph(figure = hurricane_graph)

    return html.Div(msg)




if __name__ == '__main__':
    app.run_server(debug=True)














####
