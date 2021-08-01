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
server = app.server
states = death_arrests_df['State'].unique().tolist()
ages = list(fatal_encounters_df["Subject's age"].unique())
races = fatal_encounters_df["Subject's race"].unique().tolist()
first_graph_attr = death_arrests_df.columns.tolist()[3:6]

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

)

app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'Police Crimes Dataset',

                        ),
                        html.H4(
                            'Analytical Overview',
                        )
                    ],

                    className='eight columns'
                ),
                html.A(
                    html.Button(
                        "View notebook on GitHub",
                        id="learnMore"

                    ),
                    href="https://github.com/lazyCodes7/Police-Crimes-Vizathon-",
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
                                {'label': 'Default', 'value': 'active'},
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
                                {'label': 'Default',
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
                                        html.P("Encounters"),
                                        html.H6(
                                            id="encounters_count",
                                            className="info_text"
                                        )
                                    ],
                                    id="encounters",
                                    className="pretty_container"
                                ),
                                html.Div(
                                    [
                                        html.P("Median Age"),
                                        html.H6(
                                            id="median_age",
                                            className="info_text"
                                        )
                                    ],
                                    id="age",
                                    className="pretty_container"
                                ),
                                html.Div(
                                    [
                                        html.P("Most affected gender"),
                                        html.H6(
                                            id="affected_gender",
                                            className="info_text"
                                        )
                                    ],
                                    id="gender",
                                    className="pretty_container"
                                ),
                                html.Div(
                                    [
                                        html.P("Most affected race"),
                                        html.H6(
                                            id="affected_race",
                                            className="info_text"
                                        )
                                    ],
                                    id="race",
                                    className="pretty_container"
                                ),                                

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
                        dcc.Graph(id='bar_graph')
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
                    className='pretty_container twelve columns',
                ),
  
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='hist_graph',
                            )
                    ],
                    className='pretty_container twelve columns',
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
    layout_count['title'] = 'People Killed in Fatal Encounters: ' + str(year_slider[0]) + "-" + str(year_slider[1])
    figure = dict(data=data, layout=layout_count)
    return figure

@app.callback(Output('bar_graph', 'figure'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_map(race_types, age_options, year_slider):
    filtered_df = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    data = []
    counts = fatal_encounters_df['Dispositions/Exclusions INTERNAL USE, NOT FOR ANALYSIS'].value_counts()
    keys = counts.keys()[:5]
    values = counts.values[:5]
    layout_count = copy.deepcopy(layout)
    data.append(
        dict(
            type='bar',
            name=keys,
            x=keys,
            y=values,
        )
    )
    '''fig = px.choropleth(locations=filtered_df['Location of death (state)'],
                    color=filtered_df["Subject's race"],
                    title="Race distribution for the fatal encounters",
                    color_continuous_scale='spectral_r',
                    hover_name=filtered_df['Location of death (state)'],
                    locationmode='USA-states',
                    labels={'Current Unemployment Rate':'Age Range %'},
                    scope='usa')'''
    layout_count['title'] = "Dispositions: " + str(year_slider[0]) + "-" + str(year_slider[1])
    figure = dict(data=data, layout=layout_count)

    return figure
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
    layout_aggregate['title'] = "Cause of death"
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
    layout_pie['title'] = 'Gender distribution + Top-5 states for encounters : {} to {}'.format(
        year_slider[0], year_slider[1])
    layout_pie['font'] = dict(color='#777777')
    layout_pie['legend'] = dict(
        font=dict(color='#CCCCCC', size='10'),
        orientation='h',
        bgcolor='rgba(0,0,0,0)'
    )
    figure = dict(data=data, layout=layout_pie)
    return figure

@app.callback(Output('hist_graph', 'figure'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_hist_plot(race_types, age_options, year_slider):
    layout_hist = copy.deepcopy(layout)
    filtered_df = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    '''data = [
        dict(
            type='histogram',
            x=filtered_df["Date (Year)"],
            y=filtered_df["Subject's race"],
            color=filtered_df["Cause of death"]

        )
    ]
    layout_hist['title'] = "Fatal Encounters vs Race: " + str(year_slider[0]) + str(year_slider[1])

    fig = dict(data=data)

    return fig'''
    fig = px.histogram(filtered_df, x="Date (Year)", y="Subject's race",color="Cause of death", color_discrete_sequence= px.colors.qualitative.Set2)
    return fig




@app.callback(Output('encounters_count', 'children'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_encounters_text(race_types, age_options, year_slider):
    filtered_df = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)


    dff = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    return len(dff)

@app.callback(Output('median_age', 'children'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_median_age(race_types, age_options, year_slider):
    dff = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    return int(dff["Age Range"].mean())


@app.callback(Output('affected_gender', 'children'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_most_affected_gender(race_types, age_options, year_slider):
    dff = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    most_affected = dff["Subject's gender"].value_counts().keys()
    return most_affected[0]




@app.callback(Output('affected_race', 'children'),
              [Input('race_types', 'value'),
               Input('age_options', 'value'),
               Input('year_slider', 'value')])
def update_most_affected_race(race_types, age_options, year_slider):
    dff = filter_dataframe(fatal_encounters_df,age_options, race_types, year_slider)
    most_affected = dff["Subject's race"].value_counts().keys()
    return most_affected[0]






if __name__ == '__main__':
    app.run_server(debug=True,threaded=True)