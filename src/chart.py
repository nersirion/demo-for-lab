
def set_writer(data_to_excel:dict) -> dict:
    writer = pd.ExcelWriter(save_path, engine="xlsxwriter")
    workbook = writer.book
    for i, (name, df) in enumerate(data_to_excel):
        df.to_excel(writer, sheet_name=name)
        worksheets = {name: writer.sheets[name]}
    return worksheets

def set_chart_options():
    chart=workbook.add_chart({'type': 'scatter',
                              'subtype': 'smooth'})
    chart.set_size({'x_scale': 2, 'y_scale': 2})
    chart.set_title({'name': 'Разные циклы'})
    chart.set_x_axis({'name': 'Voltage',
                      'name_font': {
                                'name': 'Times New Roman',
                                'size': 12
                                },
                      'min': 2.4,
                      'max': 4,
                      'reverse': True})
    chart.set_y_axis({'name': names[i],
                      'name_font':
                     {'name': 'Times New Roman', 'size': 12}})
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
