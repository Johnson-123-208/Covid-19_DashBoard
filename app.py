import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(DATA_URL)
df['date'] = pd.to_datetime(df['date'])
df = df[df['continent'].notna()]
countries = df['location'].unique()

# Initialize app
app = dash.Dash(
    __name__,
    assets_folder="assets",
    external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"]
)
app.title = "COVID-19 Dashboard"

# Layout
app.layout = html.Div([
    html.Div(id="particles-js"),  # Background particles

    html.Div([
        html.Div(
            className="header",
            children=[
                html.H1("🌍 COVID-19 Global Dashboard"),
                html.P("Track COVID-19 trends and vaccination progress by country.")
            ]
        ),
        html.Div(
            className="dropdown-section",
            children=[
                html.Label("Select a Country", className="dropdown-label"),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": c, "value": c} for c in countries],
                    value="India",
                    className="dropdown"
                )
            ]
        ),
        html.Div(
            className="graphs",
            children=[
                dcc.Graph(id="cases-graph", className="graph"),
                dcc.Graph(id="vaccinations-graph", className="graph"),
                dcc.Graph(id="deaths-graph", className="graph"),
                dcc.Graph(id="daily-vax-graph", className="graph"),
                dcc.Graph(id="tests-graph", className="graph"),
            ]
        )
    ], className="container")
])

# Callbacks
@app.callback(
    Output("cases-graph", "figure"),
    Output("vaccinations-graph", "figure"),
    Output("deaths-graph", "figure"),
    Output("daily-vax-graph", "figure"),
    Output("tests-graph", "figure"),
    Input("country-dropdown", "value")
)
def update_charts(selected_country):
    country_df = df[df["location"] == selected_country]

    fig_cases = px.line(
        country_df, x="date", y="new_cases",
        title=f"📊 Daily New COVID-19 Cases in {selected_country}",
        labels={"new_cases": "New Cases", "date": "Date"},
        template="plotly_white"
    )
    fig_cases.update_traces(line=dict(color="#ef4444"))

    fig_vaccinated = px.line(
        country_df, x="date", y="people_vaccinated",
        title=f"💉 People Vaccinated in {selected_country}",
        labels={"people_vaccinated": "People Vaccinated", "date": "Date"},
        template="plotly_white"
    )
    fig_vaccinated.update_traces(line=dict(color="#10b981"))

    fig_deaths = px.line(
        country_df, x="date", y="total_deaths",
        title=f"☠️ Cumulative Deaths in {selected_country}",
        labels={"total_deaths": "Total Deaths", "date": "Date"},
        template="plotly_white"
    )
    fig_deaths.update_traces(line=dict(color="#6b7280"))

    fig_daily_vax = px.line(
        country_df, x="date", y="new_vaccinations",
        title=f"📅 Daily Vaccinations in {selected_country}",
        labels={"new_vaccinations": "Daily Vaccinations", "date": "Date"},
        template="plotly_white"
    )
    fig_daily_vax.update_traces(line=dict(color="#3b82f6"))

    fig_tests = px.line(
        country_df, x="date", y="total_tests",
        title=f"🧪 Total Tests Conducted in {selected_country}",
        labels={"total_tests": "Total Tests", "date": "Date"},
        template="plotly_white"
    )
    fig_tests.update_traces(line=dict(color="#8b5cf6"))

    return fig_cases, fig_vaccinated, fig_deaths, fig_daily_vax, fig_tests

# Run
if __name__ == "__main__":
    app.run(debug=True)
