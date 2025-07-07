# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown list for Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # TASK 2: Pie chart to show successful launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    html.Br(),

    # TASK 4: Scatter chart to show correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TASK 2 & 3: Callback for pie chart updates based on dropdown and slider inputs
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_pie_chart(entered_site, payload_range):
    low, high = payload_range
    # Filter dataframe by payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        # Show total successful launches by site within payload range
        success_df = filtered_df[filtered_df['class'] == 1]
        fig = px.pie(
            success_df,
            names='Launch Site',
            title=f'Total Successful Launches for Payload Range {low} - {high} kg'
        )
    else:
        # Show success vs failure for selected site within payload range
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        pie_df = site_df.groupby('class').size().reset_index(name='count')
        pie_df['class'] = pie_df['class'].map({1: 'Success', 0: 'Failure'})

        fig = px.pie(
            pie_df,
            names='class',
            values='count',
            title=f'Success vs Failure for site {entered_site} and payload {low}-{high} kg'
        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)