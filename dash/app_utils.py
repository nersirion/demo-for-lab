import plotly.graph_objects as go
from dash_table.Format import Format
import dash_table
import pandas as pd
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input


def get_dropdown(id, values, cycle=False):
    dropdown = dcc.Dropdown(
        id=id,
        options=[{"label": f"Cycle {value}" if cycle else value, "value":value} for value in values],
        value=values[0],
        multi=True
    )
    return dropdown


def get_group(group, n_chart, axis):
    step = len(group) // 5
    if axis == "x":
        group =  group.iloc[step*n_chart:step*(n_chart+1)]
    else:
        group = group.iloc[len(group)-step:len(group)]
    return group


def get_df(df, n_chart=0):
    df_x = df.groupby("sample").apply(lambda group: get_group(group, n_chart, "x"))
    df_y = df.groupby("sample").apply(lambda group: get_group(group, n_chart, "y"))
    df = pd.concat([df_x, df_y])
    return df

def get_table(name, df):
    table = dash_table.DataTable(
        id=f"table_{name}",
        columns=[
            {"name": str(col), "id": str(col), "type": "numeric", "format":Format(precision=4)} for col in df.columns],
        data=df.to_dict("result"),
        export_format="xlsx",
        editable=True,
        row_deletable=True,
        sort_action="native",
        sort_mode="multi",
        filter_action="native",
        page_action='none',
        style_table={'height': '500px', 'overflowY': 'auto'}
    )
    return table

def get_divblock(df, name, columns, samples):
    cycle_id = f"cycle_{name}"
    cycle_dropdown = get_dropdown(cycle_id, columns, cycle=True)
    sample_id = f"sample_{name}"
    sample_dropdown = get_dropdown(sample_id, samples)
    chart = dcc.Graph(id=name)
    n_chart = get_n_chart(name)
    df = get_df(df, n_chart)
    table = get_table(name, df)
    return html.Div([html.Div([cycle_dropdown, sample_dropdown, chart], style={"width": "45%"}),
                    html.Div([table], style={"width": "45%"})])

def get_n_chart(name):
    name = name.lower()
    if name == "d":
        return 0
    elif name == "logd":
        return 1
    elif name == "rpol":
        return 2
    elif name == "rohm":
        return 3

def get_figure(rows, cycle_i, sample_value):
    df = pd.DataFrame(rows)
    if isinstance(cycle_i, list):
        cycle_s = [str(i) for i in cycle_i]
        cycles = "-".join(cycle_s)
    else:
        cycles = str(cycle_i)
        cycle_s = str(cycle_i)
    figure = go.Figure()
    for sample, group in df.groupby("sample"):
        if sample in sample_value:
            dff = group.loc[:, cycle_s]
            dff = pd.DataFrame(dff)
            y_end = len(dff) // 2
            y_start = len(dff) // 4
            x_start = len(dff) - 15
            x_start0 = len(dff) - len(dff) // 2
            for i, cycle in enumerate(dff.columns):
                figure.add_trace(go.Scatter(x=dff.iloc[x_start0:x_start, i], y=dff.iloc[:15, i], xaxis='x2', name=f"Chg_Cycle {cycle}-{sample}"))
                figure.add_trace(go.Scatter(mode="lines+markers", marker_symbol="diamond",xaxis='x1',\
                                            x=dff.iloc[x_start:, i], y=dff.iloc[y_start:y_end, i], name=f"DChg_Cycle {cycle}-{sample}"))
                figure.update_layout(
                    title={"text":f"D Cycle {cycles}",
                        },
                    height=600,
                    width=950,
                    yaxis=dict(
                        title= "D",
                        ),
                    xaxis=dict(
                        title= 'DChg_Voltage',
                        autorange="reversed",
                        showgrid=False
                    ),
                    xaxis2=dict(
                        title= 'Chg_Voltage',
                        side = 'top',
                        overlaying='x1',
                    )
                )
    return figure

