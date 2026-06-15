#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)


# In[2]:


df = pd.read_csv("data.csv")


# In[3]:


app.layout = html.Div([
    html.H1("Tableau de bord commercial", style={"textAlign": "center"}),

    html.Div([
        html.Label("Choisir une ville :"),
        dcc.Dropdown(
            id="ville",
            options=[{"label": v, "value": v} for v in df["ville"]],
            value="Abidjan",
            clearable=False
        )
    ], style={"width": "40%", "margin": "auto"}),

    html.Br(),

    html.Div([
        dcc.Graph(id="graph-ventes"),
        dcc.Graph(id="graph-profit")
    ], style={"display": "flex"}),

    html.Div([
        dcc.Graph(id="graph-population"),
        dcc.Graph(id="carte")
    ], style={"display": "flex"})
])


@app.callback(
    Output("graph-ventes", "figure"),
    Output("graph-profit", "figure"),
    Output("graph-population", "figure"),
    Output("carte", "figure"),
    Input("ville", "value")
)
def update_dashboard(ville_selectionnee):
    ville_data = df[df["ville"] == ville_selectionnee]

    fig_ventes = px.bar(
        df,
        x="ville",
        y="ventes",
        title="Ventes par ville",
        text="ventes"
    )

    fig_profit = px.pie(
        df,
        names="ville",
        values="profit",
        title="Répartition du profit par ville"
    )

    fig_population = px.scatter(
        df,
        x="population",
        y="ventes",
        size="profit",
        color="ville",
        title="Relation entre population, ventes et profit"
    )

    fig_carte = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        size="ventes",
        color="profit",
        hover_name="ville",
        hover_data=["population", "ventes", "profit"],
        zoom=5,
        height=500,
        title="Carte des villes"
    )

    fig_carte.update_layout(mapbox_style="open-street-map")

    for fig in [fig_ventes, fig_profit, fig_population, fig_carte]:
        fig.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 20})

    return fig_ventes, fig_profit, fig_population, fig_carte


server = app.server

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




