import plotly.graph_objects as go
from dash_table.Format import Format
import dash_table
import pandas as pd
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import app_utils

path = r"D:\For Wife\Source\test\gitt\all_gitt.xlsx"
df = pd.read_excel(path)

app = dash.Dash(__name__)

columns = df.columns[1:-1]
samples = df["sample"].unique()

div_d = app_utils.get_divblock(df, "d", columns, samples)

div_logd = app_utils.get_divblock(df,"logd", columns, samples)

div_rpol = app_utils.get_divblock(df, "rpol", columns, samples)

div_rohm = app_utils.get_divblock(df, "rohm", columns, samples)

app.layout = html.Div([div_d, div_logd, div_rpol, div_rohm])


@app.callback(
    Output("table_d", "data"),
    [Input("cycle_d", "value"),
     Input("sample_d", "value")])
def update_table(cycle_i, samples):
    dff = app_utils.get_df(df, 0)
    dff = dff.reset_index(drop=True)
    dff = dff.groupby("sample").filter(lambda g: g.iloc[0, -1] in samples)
    for col in dff.columns[1:-1]:
        if str(col) not in str(cycle_i):
            dff = dff.drop(col, axis=1)

    return dff.to_dict("records")

@app.callback(
    Output("d", "figure"),
    [Input("table_d", "data"),
     Input("cycle_d", "value"),
     Input("sample_d", "value")])
def update_graph_d(rows, cycle_i, sample_value):
    figure = app_utils.get_figure(rows, cycle_i, sample_value)
    return figure

@app.callback(
    Output("table_logd", "data"),
    [Input("cycle_logd", "value"),
     Input("sample_logd", "value")])
def update_table(cycle_i, samples):
    dff = app_utils.get_df(df, 1)
    dff = dff.reset_index(drop=True)
    dff = dff.groupby("sample").filter(lambda g: g.iloc[0, -1] in samples)
    for col in dff.columns[1:-1]:
        if str(col) not in str(cycle_i):
            dff = dff.drop(col, axis=1)

    return dff.to_dict("records")

@app.callback(
    Output("logd", "figure"),
    [Input("table_logd", "data"),
     Input("cycle_logd", "value"),
     Input("sample_logd", "value")])
def update_graph_d(rows, cycle_i, sample_value):
    figure = app_utils.get_figure(rows, cycle_i, sample_value)
    return figure

@app.callback(
    Output("table_rpol", "data"),
    [Input("cycle_rpol", "value"),
     Input("sample_rpol", "value")])
def update_table(cycle_i, samples):
    dff = app_utils.get_df(df, 2)
    dff = dff.reset_index(drop=True)
    dff = dff.groupby("sample").filter(lambda g: g.iloc[0, -1] in samples)
    for col in dff.columns[1:-1]:
        if str(col) not in str(cycle_i):
            dff = dff.drop(col, axis=1)

    return dff.to_dict("records")

@app.callback(
    Output("rpol", "figure"),
    [Input("table_rpol", "data"),
     Input("cycle_rpol", "value"),
     Input("sample_rpol", "value")])
def update_graph_d(rows, cycle_i, sample_value):
    figure = app_utils.get_figure(rows, cycle_i, sample_value)
    return figure

@app.callback(
    Output("table_rohm", "data"),
    [Input("cycle_rohm", "value"),
     Input("sample_rohm", "value")])
def update_table(cycle_i, samples):
    dff = app_utils.get_df(df, 3)
    dff = dff.reset_index(drop=True)
    dff = dff.groupby("sample").filter(lambda g: g.iloc[0, -1] in samples)
    for col in dff.columns[1:-1]:
        if str(col) not in str(cycle_i):
            dff = dff.drop(col, axis=1)

    return dff.to_dict("records")

@app.callback(
    Output("rohm", "figure"),
    [Input("table_rohm", "data"),
     Input("cycle_rohm", "value"),
     Input("sample_rohm", "value")])
def update_graph_d(rows, cycle_i, sample_value):
    figure = app_utils.get_figure(rows, cycle_i, sample_value)
    return figure


if __name__ == "__main__":
    app.run_server(debug=True)

