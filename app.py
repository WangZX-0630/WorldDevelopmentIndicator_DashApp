from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import os

import pandas as pd

indicators = ['Agriculture, value added (% of GDP)',
              'CO2 emissions (metric tons per capita)',
              'Domestic credit provided by financial sector (% of GDP)',
              'Electric power consumption (kWh per capita)',
              'Energy use (kg of oil equivalent per capita)',
              'Exports of goods and services (% of GDP)',
              'Fertility rate, total (births per woman)',
              'GDP growth (annual %)',
              'Imports of goods and services (% of GDP)',
              'Industry, value added (% of GDP)',
              'Inflation, GDP deflator (annual %)',
              'Life expectancy at birth, total (years)',
              'Population density (people per sq. km of land area)',
              'Services, etc., value added (% of GDP)',
              "Birth rate, crude (per 1,000 people)",
              "GDP per capita (constant 2015 US$)",
              "Merchandise exports (current US$)",
              "Population, total"]

root = os.getcwd()
df = pd.read_csv(root + "/data/part_wdi.csv")
indicator_name = indicators[0]
year_mark = {str(year): {'label': 'Year' + str(year)} for year in range(1960, 2021, 10)}
country_color_dict = dict()
for line in open(root + "/data/country_color.txt"):
    country_color_dict[line.split(' ')[0]] = line.strip('\n').split(' ')[1]

# define sunburst figure
sun_fig_data = pd.read_csv(root + '/data/sun_fig.csv')
sun_fig = go.Figure(go.Sunburst(
    ids=sun_fig_data['ids'],
    labels=sun_fig_data['labels'],
    parents=sun_fig_data['parents'],
    values=sun_fig_data['values'],
    branchvalues="total",
    insidetextorientation='radial'
))
sun_fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

df00 = df[df.Year >= 2000]
scat_df = pd.merge(df00[df.Indicator_Name == "GDP per capita (constant 2015 US$)"],
                   df00[df.Indicator_Name == 'Life expectancy at birth, total (years)'],
                   on='Country_Name', how='inner', suffixes=('_X', '_Y'))
scat_fig = go.Figure(px.scatter(scat_df.sort_values(by='Year_X'), y='Value_Y', x='Value_X',
           animation_frame='Year_X', animation_group='Country_Name',
           color='Country_Name'))
scat_fig.update_layout(transition_duration=100, height=540,
                       xaxis={'title': 'GDP per capita'},
                       yaxis={'title': 'Life expectancy'})


app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

app.title = "World Development Indicator"
app.layout = html.Div(
    # id='root',
    children=[
        html.Div(
            className='head-tab',
            children=[
                html.Br(),
                html.Div("World Development Indicator",
                        className='app-page-header'),
            ]
        ),
        html.Div(
            className='app-con',
            children=[
                html.Div(
                    className='top_boxes',
                    children=[
                        html.Div(
                            className='box-item',
                            children=[
                                html.H1(
                                    className="box-text",
                                    children="212 COUNTRIES"
                                )
                            ]
                        ),
                        html.Div(
                            className='box-item',
                            children=[
                                html.H1(
                                    className="box-text",
                                    children="1442 INDICATORS"
                                )
                            ]
                        ),
                        html.Img(src=app.get_asset_url('worldcloud.png'),
                                 id='worldcloud_pic'),
                        html.Div(
                            className='box-item',
                            children=[
                                html.H1(
                                    className="box-text",
                                    children="FROM 1960 TIL NOW"
                                )
                            ]
                        ),
                        html.Div(
                            className='box-item',
                            children=[
                                html.H1(
                                    className="box-text",
                                    children="21 TOPICS COVERED"
                                )
                            ]
                        ),
                    ]
                ),

                html.Br(style={'padding': '300px'}),

                html.Div(
                    id='app-container',
                    children=[
                        html.Div(
                            className='box',
                            children=[
                                html.Div(
                                    className="chart-dropdown",
                                    children=[
                                        html.P(
                                            "Choose one WDI indicator",
                                            className="heatmap-title"
                                        ),
                                        dcc.Dropdown(
                                            df['Indicator_Name'].unique(),
                                            "Birth rate, crude (per 1,000 people)",
                                            id='indicator_selector'
                                        )],
                                    style={'width': '40%'}
                                ),
                                html.Br(style={'margin': '100px'}),
                                html.Div(
                                    children=[
                                        html.P(
                                            "Heatmap of one WDI indicator around the World      ",
                                            className="map-title",
                                            style={'text-align': 'center'}
                                        ),
                                        dcc.Graph(id='graph-with-slider1'),
                                        dcc.Graph(id='graph-with-slider2')
                                    ]),
                                html.Div(
                                    id="slider-container",
                                    children=[
                                        html.P(
                                            id="slider-text",
                                            children="Drag the slider to change the year:",
                                        ),
                                        dcc.Slider(
                                            min=1960,
                                            max=2020,
                                            step=1,
                                            value=1960,
                                            marks=year_mark,
                                            id='year-slider',
                                            updatemode='drag',
                                            tooltip={"placement": "bottom", "always_visible": True}
                                        )
                                    ],
                                ),
                            ]),
                        html.Div(
                            className='box_two_col',
                            children=[
                                html.Div(
                                    className='scatter_box',
                                    children=[
                                        html.P(
                                            "Choose one year and two WDI indicators: ",
                                            className="heatmap-title",
                                            style={'text-align': 'center'}
                                        ),
                                        html.Div(
                                            children=[
                                                html.P("Year: ", className="heatmap-title"),
                                                dcc.Dropdown(
                                                    [i for i in range(1960, 2021)],
                                                    2010,
                                                    id='indicator-year',
                                                )
                                            ], style={'display': 'grid',
                                                      'grid-template-columns': '30% 70%',
                                                      'align-content': 'center',
                                                      'text-align': 'center'}
                                        ),
                                        html.Div(
                                            children=[
                                                html.P("Indicator X: ", className="heatmap-title"),
                                                dcc.Dropdown(
                                                    df['Indicator_Name'].unique(),
                                                    'Fertility rate, total (births per woman)',
                                                    id='xaxis-column'
                                                )
                                            ], style={'display': 'grid',
                                                      'grid-template-columns': '30% 70%',
                                                      'align-content': 'center',
                                                      'text-align': 'center'}
                                        ),
                                        html.Div(
                                            children=[
                                                html.P("Indicator Y: ", className="heatmap-title"),
                                                dcc.Dropdown(
                                                    df['Indicator_Name'].unique(),
                                                    'Life expectancy at birth, total (years)',
                                                    id='yaxis-column'
                                                )
                                            ], style={'display': 'grid',
                                                      'grid-template-columns': '30% 70%',
                                                      'align-content': 'center',
                                                      'text-align': 'center'}
                                        )
                                    ]),

                                dcc.Graph(id='indicator-graphic',
                                          style={'margin': '10px',
                                                 'padding': '10px',
                                                 'border': '1px'}
                                          ),
                            ]
                        ),
                        html.Div(
                            className='two_box_row',
                            children=[
                                html.Div(
                                    className='box',
                                    children=[
                                        html.P(
                                            "WDI consists of 6 dimensions, Covers 21 topics",
                                            className="heatmap-title"
                                        ),
                                        html.Br(),
                                        dcc.Graph(figure=sun_fig)
                                    ], style={'height': '600px'}
                                ),
                                html.Div(
                                    className='box',
                                    children=[
                                        html.P(
                                            "Life expectancy versus GDP per capita of countries in every year",
                                            className="heatmap-title"
                                        ),
                                        html.Br(),
                                        dcc.Graph(figure=scat_fig)
                                    ]
                                )
                            ]
                        )

                    ]),
            ]
        ),

        html.Br(style={'margin': '200px'})


])


@app.callback(
    Output('graph-with-slider1', 'figure'),
    Output('graph-with-slider2', 'figure'),
    Input('year-slider', 'value'),
    Input('indicator_selector', 'value'))
def update_figure(selected_year, selected_indicator):
    df1 = df[df.Indicator_Name == selected_indicator]
    filtered_df = df1[df1.Year == selected_year]

    max_scale = df1.Value.max()
    fig1 = go.Figure(
            data=go.Choropleth(
                locations=filtered_df['Country_Code'],
                z=filtered_df['Value'].astype(float),
                locationmode='ISO-3',
                colorscale='matter',
                showscale=True,
                zmax=max_scale,
                zmin=0,
                marker_line_color='rgba(0,0,0,0)',
            ),
            layout=dict(
                geo=dict(scope='world',
                         projection={'type': 'natural earth'},
                         projection_scale=1.1,
                         bgcolor='rgba(0,0,0,0)',
                         showframe=False),
                transition_duration=100,
                margin=dict(r=0, l=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)')
    )

    fdf10 = filtered_df.sort_values(by='Value', ascending=False)
    colors = [country_color_dict[i] for i in fdf10.head(15)['Country_Code']]

    fig2 = go.Figure(
        data=go.Bar(
            y=fdf10.head(15).Value,
            x=fdf10.head(15).Country_Name,
            width=0.6,
            marker_color=colors),
        layout=dict(
            transition_duration=100,
            font_size=9,
            height=400,
            autosize=True,
            yaxis_title_text=selected_indicator))

    fig_layout = fig2["layout"]
    fig_layout["xaxis"]["title"] = ""
    fig_layout["yaxis"]["fixedrange"] = True
    fig_layout["xaxis"]["fixedrange"] = False
    fig_layout["legend"] = dict(orientation="v")
    fig_layout["autosize"] = True
    fig_layout["paper_bgcolor"] = "#F9F9F8"
    fig_layout["plot_bgcolor"] = "#F9F9F8"
    # fig_layout["font"]["color"] = "#655DBB"
    # fig_layout["xaxis"]["tickfont"]["color"] = "#655DBB"
    # fig_layout["yaxis"]["tickfont"]["color"] = "#655DBB"
    # fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    # fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"

    return fig1, fig2


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('indicator-year', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['Year'] == year_value]
    dff1 = dff[dff['Indicator_Name'] == xaxis_column_name]
    dff2 = dff[dff['Indicator_Name'] == yaxis_column_name]
    dff3 = pd.merge(dff1, dff2, on='Country_Name', how='inner', suffixes=('_x', '_y'))

    fig = px.scatter(dff3, x='Value_x',
                     y='Value_y',
                     hover_name='Country_Name',
                     size=[0.5 for _ in range(len(dff3))],
                     color='Country_Name',
                     )

    fig.update_layout(height=600,
                      margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                      hovermode='closest',
                      paper_bgcolor='#F9F9F8',
                      xaxis={'title': 'Indicator_X'},
                      yaxis={'title': 'Indicator_Y'}
                      )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

