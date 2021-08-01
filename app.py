import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import copy
app = dash.Dash(__name__)
death_arrests_df = pd.read_csv('death_arrests.csv')
fatal_encounters_df = pd.read_csv('encounters.csv')

states = death_arrests_df['State'].unique().tolist()
ages = list(fatal_encounters_df["Subject's age"].unique())
races = fatal_encounters_df["Subject's race"].unique().tolist()
first_graph_attr = death_arrests_df.columns.tolist()[3:6]
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)

app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'New York Oil and Gas',

                        ),
                        html.H4(
                            'Production Overview',
                        )
                    ],

                    className='eight columns'
                ),
                html.Img(
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    className='two columns',
                ),
                html.A(
                    html.Button(
                        "Learn More",
                        id="learnMore"

                    ),
                    href="https://plot.ly/dash/pricing/",
                    className="two columns"
                )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by Date of Death:",
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='year_slider',
                            min=2000,
                            max=2020,
                            value=[2000, 2010],
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by Age of Death',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='age_selector',
                            options=[
                                {'label': 'All ', 'value': 'all'},
                                {'label': 'Active only ', 'value': 'active'},
                                {'label': 'Customize ', 'value': 'custom'}
                            ],
                            value='all',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),
                        dcc.Dropdown(
                            id='age_options',
                            options=[{'label': i, 'value': i} for i in fatal_encounters_df["Subject's age"].unique()],
                            multi=True,
                            value=fatal_encounters_df["Subject's age"].unique(),
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by race',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='race_type_selector',
                            options=[
                                {'label': 'All ', 'value': 'all'},
                                {'label': 'Productive only ',
                                    'value': 'productive'},
                                {'label': 'Customize ', 'value': 'custom'}
                            ],
                            value='productive',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),
                        dcc.Dropdown(
                            id='race_types',
                            options=[{'label': i, 'value': i} for i in races],
                            multi=True,
                            value=ages[0],
                            className="dcc_control"
                        ),
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("No. of Wells"),
                                        html.H6(
                                            id="well_text",
                                            className="info_text"
                                        )
                                    ],
                                    id="wells",
                                    className="pretty_container"
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P("Gas"),
                                                html.H6(
                                                    id="gasText",
                                                    className="info_text"
                                                )
                                            ],
                                            id="gas",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("Oil"),
                                                html.H6(
                                                    id="oilText",
                                                    className="info_text"
                                                )
                                            ],
                                            id="oil",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("Water"),
                                                html.H6(
                                                    id="waterText",
                                                    className="info_text"
                                                )
                                            ],
                                            id="water",
                                            className="pretty_container"
                                        ),
                                    ],
                                    id="tripleContainer",
                                )

                            ],
                            id="infoContainer",
                            className="row"
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='year_graph',
                                )
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map_graph')
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='pie_graph')
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='line_graph',
                            )
                    ],
                    className='pretty_container eight columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='aggregate_graph')
                    ],
                    className='pretty_container four columns',
                ),
            ],
            className='row'
        ),


    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)
def filter_dataframe(df, age_options, race_options, year_slider):
    dff = df[df["Subject's age"].isin(age_options)
             & df["Subject's race"].isin(race_options)
             & (df['Date (Year)'] > year_slider[0])
             & (df['Date (Year)'] < year_slider[1])]
    return dff

@app.callback(Output('age_options', 'value'),
              [Input('age_selector', 'value')])
def display_status(selector):
    print(selector)
    if selector == 'all':
        return ages
    elif selector == 'active':
        return ['Unknown']
    else:
        print("Go")
        return []
@app.callback(Output('race_types', 'value'),
              [Input('race_type_selector', 'value')])
def display_races(selector):
    print(selector)
    if selector == 'all':
        return races
    elif selector == 'productive':
        return [races[0]]
    else:
        print("Go")
        return []

@app.callback(Output('year_graph', 'figure'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_figure(race_types, age_options, year_slider):
    filtered_df = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)

    layout_count = copy.deepcopy(layout)
    years = filtered_df['Date (Year)'].value_counts()
    data = []
    colors = []
    for i in range(2000, 2020):
        if i >= int(year_slider[0]) and i < int(year_slider[1]):
            colors.append('rgb(123, 199, 255)')
        else:
            colors.append('rgba(123, 199, 255, 0.2)')
    data.append(
        dict(
            type='bar',
            name=races,
            x=years.keys(),
            y=years.values,
            marker=dict(
                color=colors
            ),
        )
    )
    layout_count['title'] = 'People Killed by Police'
    figure = dict(data=data, layout=layout_count)
    return figure

@app.callback(Output('map_graph', 'figure'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_map(race_types, age_options, year_slider):
    filtered_df = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    data = []
    layout_count = copy.deepcopy(layout)
    '''data.append(
        dict(
            type = 'choropleth',
            colorscale = 'Viridis',
            locations = filtered_df['Location of death (state)'],
            z = filtered_df["Age Range"],
            locationmode = 'USA-states',

        )
    )'''
    fig = px.choropleth(locations=filtered_df['Location of death (state)'],
                    color=filtered_df["Age Range"],
                    color_continuous_scale='spectral_r',
                    hover_name=filtered_df['Location of death (state)'],
                    locationmode='USA-states',
                    labels={'Current Unemployment Rate':'Age Range %'},
                    scope='usa')
    #figure = dict(data=data, layout=layout_count)

    return fig
@app.callback(Output('line_graph', 'figure'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_line_plot(race_types, age_options, year_slider):
    layout_aggregate = copy.deepcopy(layout)
    filtered_df = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    m_filtered_df = filtered_df[filtered_df["Subject's gender"] == "Male"]
    f_filtered_df = filtered_df[filtered_df["Subject's gender"] == "Female"]
    t_filtered_df = filtered_df[filtered_df["Subject's gender"]== "Transgender"]

    m_counts = m_filtered_df["Cause of death"].value_counts()
    f_counts = f_filtered_df["Cause of death"].value_counts()
    t_counts = t_filtered_df["Cause of death"].value_counts()
    data = [
        dict(
            type='scatter',
            mode='lines',
            name='Male',
            x=m_counts.keys(),
            y=m_counts.values,
            line=dict(
                shape="spline",
                smoothing="2",
                color='#F9ADA0'
            )
        ),
        dict(
            type='scatter',
            mode='lines',
            name='Female',
            x=f_counts.keys(),
            y=f_counts.values,
            line=dict(
                shape="spline",
                smoothing="2",
                color='#849E68'
            )
        ),
        dict(
            type='scatter',
            mode='lines',
            name='Transgender',
            x=f_counts.keys(),
            y=f_counts.values,
            line=dict(
                shape="spline",
                smoothing="2",
                color='#59C3C3'
            )
        ),
        

    ]
    layout_aggregate['title'] = "Cause of murder"
    figure = dict(data=data, layout=layout_aggregate)

    return figure

@app.callback(Output('pie_graph', 'figure'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_pie_plot(race_types, age_options, year_slider):
    layout_pie = copy.deepcopy(layout)
    filtered_df = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    gender = filtered_df["Subject's gender"].value_counts()
    state = filtered_df["Location of death (state)"].value_counts()
    state_labels = state.keys()[0:5]
    state_values = state.values[0:5]
    labels = gender.keys()
    values = gender.values
    data = [
            dict(
                type='pie',
                labels=labels,
                values=values,
                name='Production Breakdown',
                text=['Male', 'Female',
                        'Transgender'],
                hoverinfo="text+value+percent",
                textinfo="label+percent+name",
                hole=0.5,
                marker=dict(
                    colors=['#fac1b7', '#a9bb95', '#92d8d8']
                ),
                domain={"x": [0, .45], 'y':[0.2, 0.8]},
            ),
            dict(
                type='pie',
                labels=state_labels,
                values=state_values,
                name='Well Type Breakdown',
                hoverinfo="label+text+value+percent",
                textinfo="label+percent+name",
                hole=0.5,
                domain={"x": [0.55, 1], 'y':[0.2, 0.8]},
            )
            
    ]
    layout_pie['title'] = 'Gender distribution: {} to {}'.format(
        year_slider[0], year_slider[1])
    layout_pie['font'] = dict(color='#777777')
    layout_pie['legend'] = dict(
        font=dict(color='#CCCCCC', size='10'),
        orientation='h',
        bgcolor='rgba(0,0,0,0)'
    )
    figure = dict(data=data, layout=layout_pie)
    return figure













if __name__ == '__main__':
    app.run_server(debug=True,threaded=True)