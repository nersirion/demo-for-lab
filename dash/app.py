import plotly.graph_objects as go
import dash_table
import pandas as pd
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

path = r"D:\For Wife\Source\test\gitt\all_gitt.xlsx"
df = pd.read_excel(path, index_col=0)

app = dash.Dash(__name__)
cycle_list = dcc.Dropdown(
    id="cycle",
    options=[{"label": f"Cycle {cycle}", "value":cycle} for i, cycle in enumerate(df.columns[:-1])],
    value=11,
    multi=True

)
sample_list = dcc.Dropdown(
    id="sample",
    options=[{"label":sample, "value":sample} for sample in df["sample"].unique()],
    value=df["sample"].unique()[0],
    multi=True
)
table = dash_table.DataTable(
    id="table",
    columns=[{"name": str(cycle), "id": str(cycle)} for cycle in df.columns],
    data=pd.concat([df.iloc[:30], df.iloc[120:150]]).to_dict("result"),
    export_format="xlsx",
)
chart_2 = dcc.Graph(id="ss")
cycle_list1 = dcc.Dropdown(
    id="cycle1",
    options=[{"label": f"Cycle {cycle}", "value":cycle} for i, cycle in enumerate(df.columns[:-1])],
    value=11,
    multi=True

)
sample_list1 = dcc.Dropdown(
    id="sample1",
    options=[{"label":sample, "value":sample} for sample in df["sample"].unique()],
    value=df["sample"].unique()[0],
    multi=True
)
table = dash_table.DataTable(
    id="table",
    columns=[{"name": str(cycle), "id": str(cycle)} for cycle in df.columns],
    data=pd.concat([df.iloc[:30], df.iloc[120:150]]).to_dict("result"),
    export_format="xlsx",
)
chart_1 = dcc.Graph(id="LogD")
app.layout = html.Div([html.Div([html.Div([cycle_list, sample_list, ])],  style={'width': '49%', 'display': 'inline-block'}),
                       html.Div([chart_2, ]),
                       html.Div([html.Div([cycle_list1, sample_list1, ])],  style={'width': '49%', 'display': 'inline-block'}),
                       html.Div([chart_1, ])])

def check_sample(sample, sample_value):
    if isinstance(sample_value, list):
        return sample in sample_value
    else:
        return sample == sample_value
@app.callback(
    Output("ss", "figure"),
    [Input("cycle", "value"),
     Input("sample", "value")]
)
def update_graph(cycle_i, sample_value):
    print(sample_value)
    if isinstance(cycle_i, list):
        cycle_s = [str(i) for i in cycle_i]
        cycles = "-".join(cycle_s)
    else:
        cycles = str(cycle_i)
    figure = go.Figure()
    for sample, group in df.groupby("sample"):
        if sample in sample_value:
            dff = group.loc[:, cycle_i]
            dff = pd.DataFrame(dff)
            y_end = len(dff) // 5
            y_start = len(dff) // 10
            x_start = len(dff) - 15
            x_start0 = len(dff) - len(dff) // 5
            for i, cycle in enumerate(dff.columns):
                figure.add_trace(go.Scatter(x=dff.iloc[x_start0:x_start, i], y=dff.iloc[:15, i], xaxis='x2', name=f"Chg_Cycle {cycle}-{sample}"))
                figure.add_trace(go.Scatter(xaxis='x1', x=dff.iloc[x_start:, i], y=dff.iloc[y_start:y_end, i], name=f"DChg_Cycle {cycle}-{sample}"))
                figure.update_layout(
                    title={"text":f"D Cycle {cycles}",
                        },
                    height=600,
                    width=950,
                    yaxis=dict(
                        title = "D"
                        ),
                    xaxis=dict(
                        title= 'DChg_Voltage',
                        autorange="reversed"
                    ),
                    xaxis2=dict(
                        title= 'Chg_Voltage',
                        side = 'top',
                        overlaying='x1',
                    )
                )
    return figure

@app.callback(
    Output("LogD", "figure"),
    [Input("cycle1", "value"),
     Input("sample1", "value")]
)
def update_graph1(cycle_i, sample_value):
    if isinstance(cycle_i, list):
        cycle_s = [str(i) for i in cycle_i]
        cycles = "-".join(cycle_s)
    else:
        cycles = str(cycle_i)
    figure = go.Figure()
    for sample, group in df.groupby("sample"):
        if sample in sample_value:
            dff = group.loc[:, cycle_i]
            dff = pd.DataFrame(dff)
            step = len(dff) // 10
            x_start0 = len(dff) - step * 2
            x_start = len(dff) - step
            y_start = step * 2
            y_mid = step * 3
            y_end = step * 4
            for i, cycle in enumerate(dff.columns):
                figure.add_trace(go.Scatter(x=dff.iloc[x_start0:x_start, i], y=dff.iloc[y_start:y_start+15, i], xaxis='x2', name=f"Chg_Cycle {cycle}-{sample}"))
                figure.add_trace(go.Scatter(xaxis='x1', x=dff.iloc[x_start:, i], y=dff.iloc[y_mid:y_end, i], name=f"DChg_Cycle {cycle}-{sample}"))
                figure.update_layout(
                    title={"text":f"logD Cycle {cycles}",
                        },
                    height=600,
                    width=950,
                    yaxis=dict(
                        title = "D"
                        ),
                    xaxis=dict(
                        title= 'DChg_Voltage',
                        autorange="reversed"
                    ),
                    xaxis2=dict(
                        title= 'Chg_Voltage',
                        side = 'top',
                        overlaying='x1',
                    )
                )
    return figure
if __name__ == "__main__":
    app.run_server(debug=True)
