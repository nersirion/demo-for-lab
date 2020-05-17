
import pandas as pd
from itertools import cycle

class ExcelWriterWrapper:

    def __init__(self, save_path:str, data_to_excel:dict):
        self.writer = pd.ExcelWriter(save_path, engine="xlsxwriter")
        self.workbook = self.writer.book
        self.worksheets = self.create_worksheets(data_to_excel)

    def __call__(self, sheet_name):
        return self.worksheets[sheet_name]

    def create_worksheets(self, data_to_excel:dict) -> dict:
        worksheets = {}
        for i, (sheet_name, df) in enumerate(data_to_excel.items()):
            df.to_excel(self.writer, sheet_name=sheet_name)
            worksheets[sheet_name]=self.writer.sheets[sheet_name]
        return worksheets

    def close_writer(self):
        self.workbook.close()



class Endless:
    def __init__(self):
        self.color = cycle( ['7E3414', '34D907', 'FAEF08', 'CE07D5', '970A4C', '584089', '99A417', '0459F9'] )
        self.marker = cycle(['square', 'diamond', 'triangle', 'circle'])

    def next_color(self):
        return next(self.color)

    def next_marker(self):
        return next(self.marker)

class ChartMaker(ExcelWriterWrapper):

    def __init__(self, save_path:str, charts_list:list, place_chart:list, data_to_excel:dict):
        super().__init__(save_path, data_to_excel)
        self.charts = charts_list
        self.place_charts = place_chart
        self.generator = Endless()

    def __len__(self):
        return len(self.charts)

    def __getitem__(self, ind_chart):
        name, sheet_name, x_axis_name, y_axis_name = self.charts[ind_chart]
        names = self.charts[ind_chart]
        self.add_chart(ind_chart)
        self.add_fake_series(sheet_name, ind_chart)
        return ind_chart, name, sheet_name

    def add_chart(self, ind_chart):
        name, sheet_name, x_axis_name, y_axis_name = self.charts[ind_chart]
        chart = self.workbook.add_chart({'type': 'scatter',
                              'subtype': 'smooth'})
        chart.set_size({'x_scale': 1.2, 'y_scale': 1.2})
        chart.set_title({'name': name})
        name_font = {'name_font':{'name': 'Times New Roman', 'size': 12}}
        chart.set_x_axis(name_font)
        chart.set_y_axis(name_font)
        chart.x_axis["name"] = x_axis_name
        chart.y_axis["name"] = y_axis_name
        self(sheet_name).insert_chart(self.place_charts[ind_chart], chart)

    def add_fake_series(self, sheet_name, ind_chart):
        chart=self.workbook.charts[ind_chart]
        chart.add_series({"categories": [sheet_name, 0, 1, 0, 1],
                          "values":[sheet_name, 0, 1, 0, 1]})
