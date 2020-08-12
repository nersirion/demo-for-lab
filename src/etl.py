import os
import re
import pandas as pd
import config
from charts.final_charts import (
    FormirovkaCharts,
    GittCharts,
    get_all_charts_names_gitt,
    get_insert_cells_gitt,
)
from utils import get_dict_with_all_results_gitt, get_result_formirovka, get_result_mean
from get_data import get_df
from config import Config


def gitt_result(path: str):
    files = get_files_from_dir(path)
    config_set = Config(path)
    result = pd.DataFrame()
    for file in files:
        sample, file_path, config_set = preparing_for_charts(path, file, config_set)
        dict_to_excel = get_dict_with_all_results_gitt(file_path, config_set.config)
        config_set.add_config(dict_to_excel)
        cells_for_charts = get_insert_cells_gitt(config_set.config)
        save_path = create_save_path(path, sample, config_set.config)
        charts = get_all_charts_names_gitt(dict_to_excel["Result"])
        temp_df = get_temp_df(dict_to_excel, config_set.config, sample)
        result = pd.concat([result, temp_df])
        gitt_charts = GittCharts(
            save_path, charts, cells_for_charts, dict_to_excel, config_set.config
        )
        gitt_charts.insert_data()
        gitt_charts.close_writer()
    result.to_excel(f"{path}/result/result.xlsx")

def get_temp_df(dict_to_excel: dict, config: dict, sample: str) -> pd.DataFrame:
    temp_df = dict_to_excel["Result"]
    Umin = config["Umin"]
    Umax = config["Umax"]
    temp_df["Urange"] = f"{Umin}-{Umax}"
    temp_df["sample"] = sample
    return temp_df

def get_files_from_dir(path: str) -> list:
    files = [file for file in os.listdir(path) if os.path.isfile(f"{path}/{file}")]
    return files


def preparing_for_charts(path: str, file: str, config_set) -> tuple:
    sample = re.sub("_gene.*|_custo.*", "", file)
    config_set(sample)
    file_path = f"{path}/{file}"
    return (sample, file_path, config_set)


def create_save_path(path: str, sample: str, config_values: dict) -> str:
    Umin = config_values["Umin"]
    Umax = config_values["Umax"]
    dir_path = f"{path}/result/{Umin}-{Umax}_V"
    make_direrctory(dir_path)
    save_path = f"{dir_path}/{sample}.xlsx"
    return save_path


def make_direrctory(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def formirovka_result(path: str = config.PATH):
    files = get_files_from_dir(path)
    config_set = Config(path)
    result = pd.DataFrame()
    data_to_excel = {}
    for file in files:
        sample, file_path, config_set = preparing_for_charts(path, file, config_set)
        df = get_df(file_path)
        result = result.append(get_result_formirovka(df, config_set.config))
        data_to_excel[sample] = df
    result.to_excel(f"{path}/result/result.xlsx")
    charts = [
        ("Diffrent Cycles", sample, "Specific capacity,mA h/g", "Voltage, V")
        for sample in data_to_excel.keys()
    ]
    cells = ["I2"] * len(data_to_excel)
    save_path = f"{path}/result/charts.xlsx"
    form_chart = FormirovkaCharts(save_path, charts, cells, data_to_excel)
    form_chart.insert_data()
    form_chart.close_writer()

def mean_result(path: str):
    files = get_files_from_dir(path)
    mean_df = pd.DataFrame()
    config_set = Config(path)
    for file in files:
        sample, file_path, config_set = preparing_for_charts(path, file, config_set)
        df = get_result_mean(file_path, config_set.config)
        df['sample'] = sample
        df = df.reset_index().set_index(['sample', 'Cycle ID'])
        mean_df = pd.concat([mean_df, df])
    mean_df.to_excel(f"{path}/result/result.xlsx")
    mean_df.to_csv(f"{path}/result/result.csv")
