import get_data

PATH = r"D:\For Wife\Source\test"
class Config:
    
    def __init__(self, path):
        config_path = f"{path}/config/config.xlsx"
        self.values_for_calculate = get_data.get_data_for_calculate()

    def __call__(self, sample:str) -> tuple:
        self.config = dict(self.values_for_calculate.loc[sample])
        self.config["n_step"] = int(self.config["n_step"])

    def add_config(self, dict_to_excel:dict):
        self.config["n_cycles"] = len(dict_to_excel["Result"].columns)
        self.config["cycles"] = dict_to_excel["Result"].columns

def formirovka_result():
    files = get_files_from_dir(path)
    config = Config(path)
    for file in files:
        sample = file.replace("_gene*", "")
        m_nav = config.formirovka_config(sample) 
        df = get_data_general(file_path)
        data_to_excel = {sample: df}
        result.append(get_result_formirovka(df))
    res = pd.concat(result)
    res.to_excel()
    form_chart = FormirovkaCharts(data_to_excel)
    form_chart.insert_data()


