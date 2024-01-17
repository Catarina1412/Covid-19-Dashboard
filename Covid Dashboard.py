import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json
import urllib.request
import dash_mantine_components as dmc

CENTER_LAT,CENTER_LON= 39.24,-8.39

url="https://covid.ourworldindata.org/data/owid-covid-data.csv"
covid=pd.read_csv(url)

colunas=["iso_code","continent","location","date","population","total_cases","new_cases",
         "total_deaths","new_deaths","icu_patients","hosp_patients","new_vaccinations",
         "people_vaccinated","people_fully_vaccinated"]

df=pd.DataFrame()

for i in colunas:
  df[i]=''
  df[i]=covid[i]

df ['total_cases'] = df ['total_cases']. fillna (0)
df ['new_cases'] = df ['new_cases']. fillna (0)
df ['total_deaths'] = df ['total_deaths']. fillna (0)
df ['new_deaths'] = df ['new_deaths']. fillna (0)

df_countries=df[~df['continent'].isna()]
df_countries.isnull().sum()

df_data=df[df["location"]=="World"]

gjson = json.load(open('countries.geojson','r'))
gjson["features"][0].keys()

df_countries_=df_countries[df_countries['date'] == '2021-02-24']
df_=df[df['date'] == '2022-12-08']

select_columns= {"total_cases":"Casos Totais Confirmados       ",
                 "new_cases":"Novos Casos Confirmados  ",
                 "total_deaths":"Óbitos Totais Confirmados  ",
                 "new_deaths":"Novos Óbitos Confirmados  "}

select_country=dict()
for i in df_['location']:
    select_country[i]=i

app=dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

fig = px.choropleth_mapbox(df_countries_,locations="iso_code", color='new_cases',
                           center={"lat":39.24, "lon": -8.39},zoom=1,
                           geojson=gjson,featureidkey='properties.ISO_A3', color_continuous_scale="Redor",
                           opacity=0.5,hover_data={"total_cases":True,"new_cases":True,"new_deaths":True, "location":True})

fig.update_layout(
    coloraxis_showscale=False,
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.layout.Margin(l=0,r=0,t=0,b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)


fig2=go.Figure(layout={"template":"plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["date"],y=df_data["total_cases"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10))





labels=[]
values=[]
final_df = df_countries_.sort_values(by=['new_cases','new_deaths'], ascending=False)
for i in range(len(final_df[:10])):
    labels.append(final_df['location'].iloc[i])
    values.append(final_df['new_cases'].iloc[i])

fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hoverinfo='label+value+percent',
                        textinfo='label',
                        textposition='inside',
                        textfont=dict(size=13),
                        hole=.5,
                        rotation=45)])
fig3.update_traces(marker=dict(colors=['#a50026','#d73027','#f46d43','#fdae61','#fee090','#e0f3f8','#abd9e9','#74add1','#4575b4','#313695']))

colors = {'Vacinação Completa':'#ffffbf',
          'Vacinação Incompleta':'#fc8d59',
          'Novas Vacinações':'#91bfdb'}

fig4 = go.Figure(data=[
    go.Bar(name='Vacinação Completa', x=df_data["date"], y=df_data['people_fully_vaccinated'],marker_color='#4575b4'),
    go.Bar(name='Vacinação Incompleta', x=df_data["date"], y=df_data['people_vaccinated'],marker_color='#fc8d59'),
    go.Bar(name='Novas Vacinações', x=df_data["date"], y=df_data['new_vaccinations'],marker_color='#ffffbf'),
])

fig4.update_layout(barmode='group')


app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=app.get_asset_url('logo_covid.png'), height=50),
                html.H5("Covid-19 Dashboard"),
                dbc.Button("WORLD", color="primary", id="location-button", size="default")
            ], style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
            html.P("Escolha a data que deseja :", style={"margin-top": "40px"}),
            html.Div(id="div-test",
                     children=[
                         dmc.DatePicker(
                             id="date-picker",
                             description="You can also provide a description",
                             minDate=df_countries["date"].min(),
                             maxDate=df_countries["date"].max(),
                             value=df_countries["date"].max(),
                             style={"border": "0px solid black", "width": 560, "background-color": "#242424"},
                         )
                     ],
                ),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Novos Casos Confirmados"),
                            html.H3(style={"color": "#fc8d59"}, id="novos-casos-text"),
                            html.Span("Casos Confirmados Totais"),
                            html.H5(id="casos-totais-text"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px",
                                                           "box-shadow": "0 4px 4px 0 rgba(0,0,0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19}",
                                                           "color": "#FFFFFF"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Novos Óbitos Confirmados"),
                            html.H3(style={"color": "#de2d26"}, id="novos-obitos-text"),
                            html.Span("Óbitos Confirmados Totais"),
                            html.H5(id="obitos-totais-text"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px",
                                                           "box-shadow": "0 4px 4px 0 rgba(0,0,0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19}",
                                                           "color": "#FFFFFF"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Pacientes Hospitalizados"),
                            html.H3(style={"color": "#ef6548"}, id="pacientes-hosp-text"),
                            html.Span("Pacientes ICU"),
                            html.H5(id="pacientes-icu-text"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px",
                                                           "box-shadow": "0 4px 4px 0 rgba(0,0,0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19}",
                                                           "color": "#FFFFFF"})
                ], md=4),
            ]),
            html.Div([
                dcc.Graph(id="vaccination-graph",
                          figure=fig4,
                          style={"background-color": "#242424", "margin-top": "10px"}
                          )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H5("Top 10 Mais Casos Novos", style={"margin-top": "15px","margin-left":"72px"}),
                        dcc.Graph(
                            id='pie-chart',
                            figure=fig3,
                            style={"background-color": "#242424","margin-top": "-5px"}
                        )
                ]),
                ],md=8),
                dbc.Col([
                dbc.Card([
                        dbc.CardHeader(id="country-text"),
                        dbc.CardBody([
                            html.Span("Novos Casos:"),
                            html.H3(style={"color": "#fc8d59"}, id="top-cases-text"),
                            html.Span("Novas Mortes:"),
                            html.H3(style={"color": "#de2d26"},id="top-deaths-text"),
                        ],style={"align":"center"})
                    ], color="light", outline=True, style={"margin-top": "120px","height": "15rem","width":"10rem","margin-left":"10px",
                                                           "box-shadow": "0 4px 4px 0 rgba(0,0,0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19}",
                                                           "color": "#FFFFFF",})
            ],md=4),
        ])
        ], md=5, style={
            "padding": "25px",
            "background-color": "#242424"
            }),
        dbc.Col(
            [
                dcc.Loading(
                id="loading-1",
                type="default",
                children=[dcc.Graph(id='choropleth-map',
                                    figure=fig,
                                    style={"height": "210vh", "margin-right": "10px"})],
            ),
        ], md=7),
        dbc.Row([
            html.Div([
                html.P("Selecione que dados deseja visualizar:", style={"margin-top": "25px"}),
                dcc.RadioItems(id="type-selection",
                               options=[{"label": j, "value": i}
                                        for i, j in select_columns.items()
                                        ],
                               value="new_cases",
                               inline=True,
                               style={"margin-top": "10px","color": "white"}
                               ),
                dcc.Dropdown(id="location-selection",
                             options=[{"label": j, "value": i}
                                      for i, j in select_country.items()
                                      ],
                             value="new_cases",
                             style={"margin-top": "10px", "color": "black"}
                             ),
                dcc.Graph(id="line-graph", figure=fig2, style={
                    "background-color": "#242424",
                }),
            ], id="teste"),
        ])
    ])
    , fluid=True)


@app.callback(
    [
        Output("novos-casos-text", "children"),
        Output("casos-totais-text", "children"),
        Output("novos-obitos-text", "children"),
        Output("obitos-totais-text", "children"),
        Output("pacientes-hosp-text", "children"),
        Output("pacientes-icu-text", "children"),
    ], [Input("date-picker", "value"), Input("location-button", "children")]
)
def display_status(date, location):
    if location == "WORLD":
        df_data_on_date = df_data[df_data["date"] == date]
        print(df_data_on_date["new_cases"])
    else:
        df_data_on_date = df_countries[(df_countries["location"] == location) & (df_countries["date"] == date)]

    casos_novos = "-" if df_data_on_date["new_cases"].isna().values[
        0] else f'{int(df_data_on_date["new_cases"].values[0]):,}'.replace(",", ".")
    casos_totais = "-" if df_data_on_date["total_cases"].isna().values[
        0] else f'{int(df_data_on_date["total_cases"].values[0]):,}'.replace(",", ".")
    obitos_novos = "-" if df_data_on_date["new_deaths"].isna().values[
        0] else f'{int(df_data_on_date["new_deaths"].values[0]):,}'.replace(",", ".")
    obitos_totais = "-" if df_data_on_date["total_deaths"].isna().values[
        0] else f'{int(df_data_on_date["total_deaths"].values[0]):,}'.replace(",", ".")
    hosp_pacientes = "-" if df_data_on_date["hosp_patients"].isna().values[
        0] else f'{int(df_data_on_date["hosp_patients"].values[0]):,}'.replace(",", ".")
    icu_pacientes = "-" if df_data_on_date["icu_patients"].isna().values[
        0] else f'{int(df_data_on_date["icu_patients"].values[0]):,}'.replace(",", ".")
    return (
        casos_novos,
        casos_totais,
        obitos_novos,
        obitos_totais,
        hosp_pacientes,
        icu_pacientes,
    )


@app.callback(
    Output("line-graph", "figure"),
    [Input("type-selection", "value"), Input("location-button", "children"),Input("location-selection","value")]
)
def plot_line_graph(plot_type, location,selection):
    if location == "WORLD":
        df_data_on_location = df_data.copy()
    else:
        df_data_on_location = df[(df["location"] == location)]
    fig2 = go.Figure(layout={"template": "plotly_dark"})
    if selection == "Select" :
        fig2.add_trace(go.Scatter(x=df_data_on_location["date"], y=df_data_on_location[plot_type]))
    else:
        df_data_selection = df[(df["location"] == selection)]
        fig2.add_trace(go.Scatter(x=df_data_on_location["date"], y=df_data_on_location[plot_type], name=location))
        fig2.add_trace(go.Scatter(x=df_data_selection["date"], y=df_data_selection[plot_type], name=selection))

    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    return fig2

@app.callback(
    Output("choropleth-map", "figure"),
    [Input("date-picker", "value")]
)
def update_map(date):
    df_data_on_countries = df_countries[df_countries["date"] == date]

    fig = px.choropleth_mapbox(df_data_on_countries, locations="iso_code", geojson=gjson,
                               featureidkey='properties.ISO_A3',
                               center={"lat": CENTER_LAT, "lon": CENTER_LON},
                               zoom=1, color="new_cases", color_continuous_scale="Redor", opacity=0.5,
                               hover_data={"total_cases": True, "new_cases": True, "new_deaths": True, "location": True}
                               )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,coloraxis_showscale=False,
                      margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        country = click_data["points"][0]["customdata"][3]
        return "{}".format(country)

    else:
        return "WORLD"

@app.callback(
    Output('pie-chart','figure'),
    [Input("date-picker", "value")])

def update_pie(date):
    df_countries_ = df_countries[df_countries['date'] == date]
    labels = []
    values = []
    final_df = df_countries_.sort_values(by=['new_cases'], ascending=False)
    for i in range(len(final_df[:10])):
        labels.append(final_df['location'].iloc[i])
        values.append(final_df['new_cases'].iloc[i])

    fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hoverinfo='label+value+percent',
                                  textinfo='label',
                                  textposition='inside',
                                  textfont=dict(size=13),
                                  hole=.5,
                                  rotation=45)])
    fig3.update_traces(marker=dict(
        colors=['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee090', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4',
                '#313695']))

    fig3.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        showlegend=False,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    return fig3
@app.callback(
        Output("top-cases-text", "children"),
        Output("top-deaths-text", "children"),
        Output("country-text","children"),
        [Input("pie-chart", "clickData"), Input("pie-chart", "n_clicks"),Input("date-picker", "value")])

def update_pie_card(data_click,clicks,date):
    df_countries_ = df_countries[(df_countries['date'] == date)]
    final_df = df_countries_.sort_values(by=['new_cases','new_deaths'], ascending=False)

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if data_click is not None and changed_id != "pie-chart.n_clicks":
        country = data_click["points"][0]["label"]
        final_df_=final_df[(final_df["location"] == country)]
        casos_novos=f'{int(final_df_["new_cases"].values[0]):,}'.replace(",", ".")
        obitos_novos=f'{int(final_df_["new_deaths"].values[0]):,}'.replace(",", ".")

    else:
        country=final_df['location'].iloc[0]
        casos_novos = f'{int(final_df["new_cases"].iloc[0]):,}'.replace(",", ".")
        obitos_novos = f'{int(final_df["new_deaths"].iloc[0]):,}'.replace(",", ".")

    return (casos_novos,obitos_novos,country)
@app.callback( Output("vaccination-graph", "figure"),
               [Input("location-button", "children")],Input("date-picker", "value"))
def update_vaccination(location,date):
    if location == "WORLD":
        df_data_on_location_ = df_data.copy()
    else:
        df_data_on_location_ = df[(df["location"] == location)]
    df_data_on_location=df_data_on_location_.sort_values(by='date')
    df_date=df_data_on_location[df_data_on_location['date']<=date]
    df_week=df_date[len(df_date['date'])-14:]


    fig4 = go.Figure(data=[
        go.Bar(name='Vacinação Completa', x=df_week["date"], y=df_week['people_fully_vaccinated'],marker_color='#4575b4'),
        go.Bar(name='Vacinação Incompleta', x=df_week["date"], y=df_week['people_vaccinated'],marker_color='#fc8d59'),
        go.Bar(name='Novas Vacinações', x=df_week["date"], y=df_week['new_vaccinations'],marker_color='#ffffbf')])

    fig4.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                color="white")
        ),
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    fig4.update_xaxes(color='white')
    fig4.update_yaxes(color='white')

    return fig4

if __name__ == "__main__":
  app.run_server(debug=False)