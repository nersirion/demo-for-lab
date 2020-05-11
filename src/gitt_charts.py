
class GittCharts(ChartMaker):

    def __init__(self):
        super().__init__()
        self.cycles = data_to_excel["Result"].columns()

    def insert_data(self):
        cycles = len(self.cycles)
        for num_chart, (name, sheet_name) in self:
            num__chart = correct_num_chart()
            chart = self.workbook.charts[ind_chart]
            update_chart(chart)
            self.add_series()

    def add_series(self):
        for num_series in range(get_number()):
            add_series_with_default_options(chart)
            series = chart.series[num_series]
            update_series(series)

    def update_legend(self, series):
        if name == "Diffrent Cycle":
            series["name"] = f"Cycle {self.cycles[num_series]}"
        elif name == "Diffrent Titr":
            series["name"] = f"Titr {num_series+1}"


def correct_num_chart() -> int:
    if name == "Diffrent Titr":
        return num_chart - 4
    elif sheet_name == "Voltage":
        return num_chart - 8
    elif sheet_name == "sqrttime":
        return num_chart - cycles - 8

def get_number() -> int:
    if name == "Diffrent Cycle":
        return cycle
    elif name == "Diffrent Titr":
        return n_step
    else:
        return 1

def update_chart(chart):
    min_axis = Umin - 0.1 
    max_axis = Umax + 0.2
    update_min_max(chart, min_axis, max_axis)

def update_min_max(chart, min_axis:float, max_axis:float):
    if name == "Diffrent Cycle":
        chart.x_axis["min"] = min_axis
        chart.x_axis["max"] = max_axis
        chart.x_axis["reverse"] == True
    elif name.startswith("Cycle"):
        chart.y_axis["min"] = min_axis
        chart.y_axis["max"] = max_axis

def update_series(series):
    update_categories_and_values(series, name, sheet_name, num_chart, num_series)
    update_marker_and_fill(series, sheet_name)
    update_legend(series, name)


def update_marker_and_fill(series):
    if sheet_name == "Result":
        series["marker"] = {"type": next(gen.marker())}
        series["fill" ]= {"color": next(gen.color())}


def update_categories_and_values(series):
    row_start, row_end, col_start, col_end = get_row_col_index_categories(name) 
    series["categories"] = [sheet_name, row_start, col_start, row_end, col_end]
    row_start, row_end, col_start, col_end = get_row_col_index_values(name) 
    series["values"] = [sheet_name, row_start, col_start, row_end, col_end]

def get_row_col_index_values() -> tuple:
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

def get_row_col_index_categories() -> tuple:
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
        



