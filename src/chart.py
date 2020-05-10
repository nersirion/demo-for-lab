
class ExcelWriterWrapper:
    
    def __init__(self, save_path:str, data_to_excel:dict):
        self.writer = pd.ExcelWriter(save_path, engine="xlsxwriter")
        self.workbook = writer.book
        self.worksheets = create_worksheets(data_to_excel)

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

def set_standart_chart_options(workbook, name:str):
    workbook.add_chart({'type': 'scatter',
                              'subtype': 'smooth'})
    chart.set_size({'x_scale': 1.6, 'y_scale': 1.4})
    chart.set_title({'name': name})
    name_font = {'name_font':{'name': 'Times New Roman', 'size': 12}}
    chart.set_x_axis(name_font)
    chart.set_y_axis(name_font)

def add_series_with_default_options():
    generator = Endless()
    chart.add_series({'line': {"width": 4},
                      "smooth": True,
                      "marker": next(generator.marker()),
                      "size": 6,
                      "border": {"color": "black"},
                      "fill": {'color': next(generator.color()))}})

def add_data_on_chart():
    data = chart.series[ind_series] 
    data['name'] = f'{data_for_charts['line']}/{name}'
    data['categoreies'] = None
    data['values'] = None
    

def set_chart_options():
    chart.set_title({'name': 'Разные циклы'})
    chart.set_x_axis({'name': 'Voltage',
                      'min': 2.4,
                      'max': 4,
                      'reverse': True})
    chart.set_y_axis({'name': names[i],
    worksheet.insert_chart('N'+str(30+i*30), chart) 

def add_data_on_chart():
    chart.add_series({'name':       'Cycle '+str(cycle_list[j]),
                      'categories': ['Result', 4*steps+1, j+1, 5*steps, j+1],
                      'values':     ['Result', steps*i+1, j+1, steps*(i+1), j+1],
                      'line':   {'width': 4},
                      'smooth': True,
                      'marker': {'type': mrk[j],
                      'size': 7,
                      'border': {'color': 'black'},
                      'fill':   {'color': clr[j]}},
        })


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
    
    def __init__(self, charts_list:list, chart_parametrs:dict):
        super().__init__()
        self.charts = charts_list

    def __len__(self):
        return len(self.charts)

    def __getitem__(self, ind_chart):
        name = self.charts[ind_chart][0]
        self.add_chart(name)
        x_axis_name = self.charts[ind_chart][1]
        y_axis_name =self.charts[ind_chart][2]
        return (x_axis_name, y_axis_name)

    def add_chart(self, name):
        set_standart_chart_options(self.workbook ,name)

class GittCharts(ChartMaker):
    
    def get_categories(self, )

    def insert_data(self):
        for i, (x_axis_name, y_axis_name) in enumerate(self):
            chart = self.workbook.charts[i]
            update_chart(chart)
            for j in range():
                add_series_with_default_options(chart)
                update_series


