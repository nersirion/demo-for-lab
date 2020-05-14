from itertools import product
import string
import pandas as pd
from charts.charts import ChartMaker

def get_charts_names_gitt_result() -> list:
    names_and_y = [("Diffrent Cycles", "Volatge"), ("Diffrent Titr", "Cycles")] 
    x_axis = ["D", "LogD", "Rpol", "Rohm"]
    charts=[(name, "Result", x, y) for (name, y) in names_and_y for x in x_axis ]
    return charts

def get_charts_names_voltage_gitt(df:pd.DataFrame) -> list:
    cycles = df.columns
    sheets_and_x = [("time", "Voltage"), ("sqrttime", "sqrttime")]
    charts_vol = [(f"Cycle {cycle}", sheet, x, "Voltage") for (x, sheet) in sheets_and_x for cycle in cycles]
    return charts_vol

def get_all_charts_names_gitt(df:pd.DataFrame) -> list:
    charts_res = get_charts_names_gitt_result()
    charts_vol = get_charts_names_voltage_gitt(df)
    charts = charts_res + charts_vol
    return charts

def get_insert_cells_gitt(config_values:dict) -> list:
    r = range(2, 28*4, 28)
    symb = ["N", "AD"]
    result_cells = [f"{s}{n}" for s in symb for n in r]
    r = range(2, 28*config_values["n_cycles"], 28)
    voltage_cells = [f"R{i}" for i in r]
    all_cells = result_cells + voltage_cells
    return all_cells

class GittCharts(ChartMaker):

    def __init__(self, save_path:str, charts_list:list, place_chart:list, data_to_excel:dict, config_values:dict):
        super().__init__(save_path, charts_list, place_chart, data_to_excel)
        self.config = config_values

    def insert_data(self):
        for num_chart, name, sheet_name in self:
            print(num_chart, name, sheet_name)
            num__chart = correct_num_chart(name, sheet_name, num_chart, self.config["n_cycles"])
            chart = self.workbook.charts[num_chart]
            update_chart(chart, name, self.config)
            self.add_series(chart, name, sheet_name, num_chart)

    def add_series(self, chart, name:str, sheet_name:str, num_chart:int):
        n_step = self.config["n_step"]
        del chart.series[0]
        for num_series in range(get_number(name, n_step)):
            add_series_with_default_options(chart, self.generator)
            series = chart.series[num_series]
            update_series(series, name, sheet_name, num_series, n_step, num_chart)
            print(chart.series[num_series])

    def update_legend(self, series):
        if name == "Diffrent Cycle":
            series["name"] = f"Cycle {self.cycles[num_series]}"
        elif name == "Diffrent Titr":
            series["name"] = f"Titr {num_series+1}"


def add_series_with_default_options(chart, generator):
    chart.add_series({'line': {"width": 4},
                      "smooth": True,
                      "marker":{"type": generator.next_marker()},
                      "size": 6,
                      "border": {"color": "black"},
                      "fill": {'color': generator.next_color()},
                      "categories": ["fake", 0,0,0,1],
                      "values": ["fake", 1,1,1,1]})
    print(chart.series)

def correct_num_chart(name:str, sheet_name:str, num_chart:int, n_cycles:int) -> int:
    if name == "Diffrent Titr":
        return num_chart - 4
    elif sheet_name == "Voltage":
        return num_chart - 8
    elif sheet_name == "sqrttime":
        return num_chart - n_cycles - 8

def get_number(name:str, n_step:int) -> int:
    if name == "Diffrent Cycle":
        return cycle
    elif name == "Diffrent Titr":
        return n_step
    else:
        return 1

def update_chart(chart, name:str, config_values:dict):
    min_axis = config_values["Umin"]- 0.1 
    max_axis = config_values["Umax"] + 0.2
    update_min_max(chart, name, min_axis, max_axis)

def update_min_max(chart, name:str, min_axis:float, max_axis:float):
    if name == "Diffrent Cycle":
        chart.x_axis["min"] = min_axis
        chart.x_axis["max"] = max_axis
        chart.x_axis["reverse"] == True
    elif name.startswith("Cycle"):
        chart.y_axis["min"] = min_axis
        chart.y_axis["max"] = max_axis

def update_series(series, name:str, sheet_name:str, num_series:int, n_step:int, num_chart:int):
    update_categories_and_values(series, name, sheet_name, num_series, n_step, num_chart)
    update_marker_and_fill(series, sheet_name)
    update_legend(series, name)


def update_marker_and_fill(series, sheet_name:str):
    if sheet_name == "Result":
        series["marker"] = {"type": next(gen.marker())}
        series["fill" ]= {"color": next(gen.color())}

ABC = string.ascii_uppercase
def update_categories_and_values(series, name:str, sheet_name:str, num_series:int, n_step:int, num_chart:int):
    row_start, row_end, col_start, col_end = get_row_col_index_categories(name, num_series, n_step, num_chart) 
    categories_str = f"{sheet_name}!${ABC[col_start]}${row_start}:${col_end}${row_end}"
    series["categories"] = categories_str
    row_start, row_end, col_start, col_end = get_row_col_index_values(name, num_series, n_step, num_chart) 
    values_str = f"{sheet_name}!${ABC[col_start]}${row_start}:${col_end}${row_end}"
    series["values"] = values_str

def get_row_col_index_values(name:str, num_series:int, n_step:int, num_chart:int) -> tuple:
    if name == "Diffrent Cycle":
        row_start = n_step * num_series + 1
        row_end = n_step * (num_series + 1)
        col_start = num_chart + 1
        col_end = num_chart + 1
        return (row_start, row_end, col_start, col_end)
    elif name == "Diffrent Titr":
        row_start = num_series * n_step + num_chart + 1
        row_end = num_series * n_step + num_chart + 1
        col_start = 1
        col_end = cycles
        return (row_start, row_end, col_start, col_end)
    row_start = 1
    row_end = len(df) + 1
    col_start = num_chart + 1
    col_end = num_chart + 1
    return (row_start, row_end, col_start, col_end) 

def get_row_col_index_categories(name:str, n_step:int) -> tuple:
    if name == "Diffrent Cycle":
        row_start = 4 * n_step + 1
        row_end = 5 * n_step
        col_start = num_chart + 1
        col_end = num_chart + 1
        return (row_start, row_end, col_start, col_end)
    elif name == "Diffrent Titr":
        row_start = 0
        row_end = 0
        col_start = 0
        col_end = cycles
        return (row_start, row_end, col_start, col_end)
    row_start = 1
    row_end = len(df) + 1
    col_start = cycles + 1
    col_end = cycles + 1
    return (row_start, row_end, col_start, col_end) 
        
"""
class FormirovkaCharts(ChartMaker):
    
    def __init__(self):
        super().__init__()
        self.cycles = data_to_excel[file]["Cycle ID"].unique()
        self.ind_chg = 
        self.ind_dchg =
        self.last_index =
    def insert_data(self):
        for num_chart, (name, sheet_name) in self:
            chart = self.workbook.charts[num_chart]
            add_series()

    def add_series(self):
        for i, cycle in enumerate(self.cycles):
            get_series(chart, title="Cycle Chg")
            get_series(chart, title="Cycle Dchg")


        

def set_categories_and_values(title:str):
        row_start, row_end = get_row_number(title)
        series["categories"] = [sheet_name, row_start, 6, row_end, 6]]
        series["values"] = [sheet_name, row_start, 4, row_end, 4]

def set_series_setings(chart, title:str):
    chart._add_series()
    series["name"] = f"{title} {cycle}"
    series["line"] = {"width": 4, "color": next(generator.color())}
    series["smooth"] = True


def get_series(chart, title:str):
    set_series_setings(chart, title:str)
    set_categories_and_values(title:str)
    
def get_row_col(title:str) -> tuple:
    if title == "Cycle Chg":
        row_start = ind_chg[i] + 2
        row_end = ind_dchg[i]
    else:
        row_start = ind_dchg[i] + 2
        row_end = last_index[i] + 2
    return (row_start, row_end)
"""
