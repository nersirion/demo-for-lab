import os
import re
import config
from charts.final_charts import (
    GittCharts,
    get_all_charts_names_gitt,
    get_insert_cells_gitt,
)
from utils import get_dict_with_all_results_gitt
from get_data import get_data_for_calculate
from config import Config


def gitt_result(path: str = config.PATH):
    files = get_files_from_dir(path)
    config_set = Config(path)
    for file in files:
        sample = re.sub("_gene.*", "", file)
        config_set(sample)
        file_path = f"{path}/{file}"
        dict_to_excel = get_dict_with_all_results_gitt(file_path, config_set.config)
        config_set.add_config(dict_to_excel)
        cells_for_charts = get_insert_cells_gitt(config_set.config)
        save_path = create_save_path(path, sample, config_set.config)
        charts = get_all_charts_names_gitt(dict_to_excel["Result"])
        gitt_charts = GittCharts(
            save_path, charts, cells_for_charts, dict_to_excel, config_set.config
        )
        gitt_charts.insert_data()
        print(save_path)
        gitt_charts.close_writer()


def get_files_from_dir(path: str) -> list:
    files = [file for file in os.listdir(path) if os.path.isfile(f"{path}/{file}")]
    return files


def preparing_for_charts(file: str) -> dict:
    sample = re.sub("_gene*", "", file)
    n_step, I, tau, S, V, M, m, Umin, Umax = config_set(sample)
    file_path = f"{path}/{file}"
    dict_to_excel = get_all_results_gitt(file_path)
    return (dict_to_excel, sample, n_step, I, tau, S, V, M, m, Umin, Umax)


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
