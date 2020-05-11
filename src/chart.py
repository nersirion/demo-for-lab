
class ExcelWriterWrapper:
    
    def __init__(self, save_path:str, data_to_excel:dict):
        self.writer = pd.ExcelWriter(save_path, engine="xlsxwriter")
        self.workbook = writer.book
        self.worksheets = self.create_worksheets(data_to_excel)

    def __call__(self, name):
        return self.worksheets["name"]

    @classmethod
    def create_worksheets(cls, data_to_excel:dict) -> dict:
        for i, (name, df) in enumerate(data_to_excel):
            df.to_excel(writer, sheet_name=name)
            worksheets = {name: writer.sheets[name]}
        return worksheets

    def close_writer(self):
        self.writer.close()


def add_series_with_default_options():
    chart.add_series({'line': {"width": 4},
                      "smooth": True,
                      "marker": next(generator.marker()),
                      "size": 6,
                      "border": {"color": "black"},
                      "fill": {'color': next(generator.color()))}})


class Endless:
    def __init__(self):
        self.color = cycle(['square', 'diamond', 'triangle', 'circle'])
        self.marker = cycle(['FF0000','00FF00','0404B4','8A0886','DF7401'])
        
    def __getitem__(self, ind):
        return 
    def next_color(self):
        return next(self.color)

    def next_marker(self):
        return next(self.marker)

class ChartMaker(ExcelWriterWrapper):
    
    def __init__(self, charts_list:list):
        super().__init__()
        self.charts = charts_list

    def __len__(self):
        return len(self.charts)

    def __getitem__(self, ind_chart):
        name, sheet_name, x_axis_name, y_axis_name = self.charts[ind_chart]
        generator = Endless()
        self.add_chart(self.workbook)
        return ind_chart, name, sheet_name

    def add_chart(self, workbook):
        workbook.add_chart({'type': 'scatter',
                              'subtype': 'smooth'})
        chart.set_size({'x_scale': 1.6, 'y_scale': 1.4})
        chart.set_title({'name': name})
        name_font = {'name_font':{'name': 'Times New Roman', 'size': 12}}
        chart.set_x_axis(name_font)
        chart.set_y_axis(name_font)
        chart.x_axis["name"] = x_axis_name
        chart.y_axis["name"] = y_axis_name
        self(sheet_name).insert_chart(place_chart[ind_chart], chart)
