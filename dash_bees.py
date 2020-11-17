import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)



# Import csv into pandas
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])


# Laying out the app Dash core component and HTML

app.layout = html.Div([html.H1("web application for dying bees", style = {'text-align':'center'}),
                       dcc.Dropdown(id="slct_year", options = [
                               {"label": "2015", "value": 2015},
                               {"label": "2016", "value": 2016},
                               {"label": "2017", "value": 2017},
                               {"label": "2018", "value": 2018}], multi =False, value=2015,style={'width': "40%"}),
html.Div(id='output_container',children=[]), html.Br(), 
dcc.Graph(id='my_bee_map', figure={})])

# Connecting plotly graphs with dash core components with callback function

@app.callback(
        [Output(component_id='output_container', component_property = 'children'),
         Output(component_id='my_bee_map', component_property = 'figure')],
        [Input(component_id='slct_year', component_property = 'value')])


def graph_update(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    container = "The year chosen by user is: {}".format(option_slctd)
    
    df_copy = df.copy()
    df_copy = df_copy[df_copy["Year"] == option_slctd]
    df_copy = df_copy[df_copy["Affected by"] == "Varroa_mites"]
    
    # creating graph using plotly express

    fig = px.choropleth(
            data_frame=df_copy,
            locationmode='USA-states',
            locations='state_code',
            scope='usa',
            color='Pct of Colonies Impacted',
            hover_data=['State', 'Pct of Colonies Impacted'],
            color_continuous_scale= px.colors.sequential.YlOrRd,
            labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
            template='plotly_dark')

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)