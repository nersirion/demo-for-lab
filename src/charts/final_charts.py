from itertools import product
import pandas as pd
from charts.charts import ChartMaker

def get_charts_names_gitt_result() -> list:
    names_and_x = [("Diffrent Cycles", "Voltage"), ("Diffrent Titr", "Cycles")]
    y_axis = ["D", "LogD", "Rpol", "Rohm"]
    charts=[(name, "Result", x, y) for (name, x) in names_and_x for y in y_axis ]
    return charts

def get_charts_names_voltage_gitt(df:pd.DataFrame) -> list:
    cycles = df.columns.astype(int)
    sheets_and_x = [("time", "Voltage"), ("sqrttime", "sqrttime")]
    charts_vol = [(f"Cycle {cycle}", sheet, x, "Voltage") for (x, sheet) in sheets_and_x for cycle in cycles]
    return charts_vol

def get_all_charts_names_gitt(df:pd.DataFrame) -> list:
    charts_res = get_charts_names_gitt_result()
    charts_vol = get_charts_names_voltage_gitt(df)
    charts = charts_res + charts_vol
    return charts

def get_insert_cells_gitt(config_values:dict) -> list:
    r = range(2, 18*4, 18)
    symb = ["N", "X"]
    result_cells = [f"{s}{n}" for s in symb for n in r]
    r = range(2, 18*config_values["n_cycles"], 18)
    voltage_cells = [f"R{i}" for i in r]
    all_cells = result_cells + voltage_cells * 2
    return all_cells

class GittCharts(ChartMaker):

    def __init__(self, save_path:str, charts_list:list, place_chart:list, data_to_excel:dict, config_values:dict):
        super().__init__(save_path, charts_list, place_chart, data_to_excel)
        self.config = config_values

    def insert_data(self):
        for num_chart, name, sheet_name in self:
            chart = self.workbook.charts[num_chart]
            num_chart = correct_num_chart(name, sheet_name, num_chart, self.config["n_cycles"])
            update_chart(chart, name, self.config)
            self.add_series(chart, name, sheet_name, num_chart)

    def add_series(self, chart, name:str, sheet_name:str, num_chart:int):
        del chart.series[0]
        for num_series in range(self.get_number(name)):
            add_series_with_default_options(chart, self.generator, name, sheet_name, num_series, num_chart, self.config)
            series = chart.series[num_series]
            update_series(series, name, sheet_name, num_series, self.config, self.generator)

    def get_number(self, name:str) -> int:
        if name == "Diffrent Cycles":
            return self.config["n_cycles"]
        elif name == "Diffrent Titr":
            return self.config["update_n_step"]
        else:
            return 1



def update_legend(series, name:str, num_series:int, config_values:dict):
    if name == "Diffrent Cycles":
        n_cycle = config_values["cycles"][num_series]
        series["name"] = f"Cycle {n_cycle}"
    elif name == "Diffrent Titr":
        series["name"] = f"Titr {num_series+1}"
    else:
        series["name"] = None


def add_series_with_default_options(chart, generator, name:str, sheet_name:str, num_series:int, num_chart:int, config_values:dict):
    categories, values = get_categories_and_values(name, sheet_name, num_series, num_chart, config_values)
    chart.add_series({"categories": categories,
                      "values": values,
                      'line': {"width": 4},
                      "smooth": True,
                      "marker":{"type": generator.next_marker(),
                                "size": 6,
                                "border": {"color": "black"},
                                "fill": {'color': generator.next_color()}}})

def correct_num_chart(name:str, sheet_name:str, num_chart:int, n_cycles:int) -> int:
    if name == "Diffrent Titr":
        return num_chart - 4
    elif sheet_name == "Voltage":
        return num_chart - 8
    elif sheet_name == "sqrttime":
        return num_chart - n_cycles - 8
    else:
        return num_chart

def update_chart(chart, name:str, config_values:dict):
    min_axis = config_values["Umin"]- 0.1
    max_axis = config_values["Umax"] + 0.2
    update_min_max(chart, name, min_axis, max_axis)

def update_min_max(chart, name:str, min_axis:float, max_axis:float):
    if name == "Diffrent Cycles":
        chart.x_axis["min"] = min_axis
        chart.x_axis["reverse"] = True
    elif name.startswith("Cycle"):
        chart.y_axis["min"] = min_axis
        chart.y_axis["max"] = max_axis
        chart.set_legend({'none': True})

def update_series(series, name:str, sheet_name:str, num_series:int, config_values:dict, generator):
    update_marker_and_fill(series, sheet_name, generator)
    update_legend(series, name, num_series, config_values)


def update_marker_and_fill(series, sheet_name:str, generator):
    if sheet_name == "Voltage" or sheet_name == "sqrttime":
        marker = series["marker"]
        marker["type"] = "circle"
        marker["size"] = 5
        marker["border"] =  {"color": "FF0000"}
        marker["fill"] = {"color": "FF0000", "defined": True}


def get_categories_and_values(name:str, sheet_name:str, num_series:int, num_chart:int, config_values:dict):
    row_start, row_end, col_start, col_end = get_row_col_index_values(name, num_series, num_chart, config_values)
    values = [sheet_name, row_start, col_start, row_end, col_end]
    row_start, row_end, col_start, col_end = get_row_col_index_categories(name, num_series, num_chart, config_values)
    categories = [sheet_name, row_start, col_start, row_end, col_end]
    return (categories, values)

def get_row_col_index_values(name:str, num_series:int, num_chart:int, config_values:dict) -> tuple:
    if name == "Diffrent Cycles":
        row_start = config_values["update_n_step"] * num_chart + 1
        row_end = config_values["update_n_step"] * (num_chart + 1)
        col_start = num_series + 1
        col_end = num_series + 1
        return (row_start, row_end, col_start, col_end)
    elif name == "Diffrent Titr":
        row_start = num_chart * config_values["update_n_step"] + num_series + 1
        row_end = num_chart * config_values["update_n_step"] + num_series + 1
        col_start = 1
        col_end = config_values["n_cycles"]
        return (row_start, row_end, col_start, col_end)
    row_start = 1
    row_end = config_values["len_df"]+ 1
    col_start = num_chart + 1
    col_end = num_chart + 1
    return (row_start, row_end, col_start, col_end)

def get_row_col_index_categories(name:str, num_series:int, num_chart:int, config_values:dict) -> tuple:
    if name == "Diffrent Cycles":
        row_start = 4 * config_values["update_n_step"] + 1
        row_end = 5 * config_values["update_n_step"]
        col_start = num_series + 1
        col_end = num_series + 1
        return (row_start, row_end, col_start, col_end)
    elif name == "Diffrent Titr":
        row_start = 0
        row_end = 0
        col_start = 0
        col_end = config_values["n_cycles"]
        return (row_start, row_end, col_start, col_end)
    row_start = 1
    row_end =  config_values["len_df"]+ 1
    col_start = config_values["n_cycles"]+ 1
    col_end = config_values["n_cycles"]+ 1
    return (row_start, row_end, col_start, col_end)


class FormirovkaCharts(ChartMaker):

    def __init__(
        self, save_path:str, charts_list:list, place_chart:list, data_to_excel:dict
    ):
        super().__init__(save_path, charts_list, place_chart, data_to_excel)
        self.data = data_to_excel
        self.color = [self.generator.next_color() for i in range(12)]

    def insert_data(self):
        for num_chart, name, sheet_name in self:
            chart = self.workbook.charts[num_chart]
            chart.y_axis["min"] = 2
            self.add_series(sheet_name, chart)

    def add_series(self, sheet_name, chart):
        cycles = self.data[sheet_name]["Cycle ID"].unique()[:-1]
        ind_df = self.get_index_for_charts(self.data[sheet_name])
        del chart.series[0]
        for i, cycle in enumerate(cycles):
            self.get_series(chart, sheet_name, cycle, "Cycle Chg", ind_df, i)
            self.get_series(chart, sheet_name, cycle, "Cycle Dchg", ind_df, i)

    def get_index_for_charts(self, df: pd.DataFrame) -> pd.DataFrame:
        ind_df = df.groupby(['Cycle ID', 'Record ID'])\
            .apply(lambda x: x.index[0] + 1)\
            .unstack('Cycle ID')\
            .iloc[:, :-1]
        ind_df.index = ["chg", "dchg", "last"]
        last_index = df[df['Record ID'] == 'CC_DChg'].groupby(['Cycle ID'])\
            .apply(lambda x: x.index[-1] + 1)
        ind_df.loc["last"] = last_index
        print(ind_df)
        return ind_df

    def get_series(
        self, chart, sheet_name: str, cycle: int, title:str, ind_df: pd.DataFrame, num_series: int
    ):
        row_start, row_end = get_row_number(title, cycle, ind_df)
        chart.add_series({
            "categories": [sheet_name, row_start, 6, row_end, 6],
            "values": [sheet_name, row_start, 4, row_end, 4],
            "name": f"{title} {cycle}",
            "line": {"widthf}": 4, "color": self.color[num_series]},
            "smooth": True })



def set_categories_and_values(
    chart, sheet_name: str, cycle: int, title:str, ind_df: pd.DataFrame
):
    row_start, row_end = get_row_number(title, cycle, ind_df)
    chart.add_series({
        "categories": [sheet_name, row_start, 5, row_end, 5],
        "values": [sheet_name, row_start, 3, row_end, 3],
        "name":  f"{title} {cycle}",
        "line": {"widthf}": 4, "color": generator.next_color()},
        "smooth": True })

def set_series_setings(series, title:str, cycle: int, generator):
    series["name"] = f"{title} {cycle}"
    print(series["line"])
    series["line"] = {"width": 4, "color": generator.next_color()}
    series["smooth"] = True




def get_row_number(title: str, cycle: int, ind_df: pd.DataFrame) -> tuple:
    if title == "Cycle Chg":
        row_start = ind_df.loc["chg", cycle]
        row_end = ind_df.loc["dchg", cycle] - 1
    else:
        row_start = ind_df.loc["dchg", cycle]
        row_end = ind_df.loc["last", cycle]
    return (row_start, row_end)
