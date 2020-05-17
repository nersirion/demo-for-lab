from collections import Counter
import functools
import math
import pandas as pd
import numpy as np
from get_data import *


def find_gitt_cycle(df: pd.DataFrame, config_values: dict) -> pd.DataFrame:
    return df.groupby("Cycle ID").filter(
        lambda x: counting_record_id_in_cycle(x)["CC_DChg"] == config_values["n_step"]
    )


def counting_record_id_in_cycle(df):
    cycle_list = df["Cycle ID"].unique().astype(int)
    counting_steps = df[df["Cycle ID"] == cycle_list[0]].groupby(
        ["Step ID", "Record ID"]
    )
    counting_steps = (
        counting_steps.nunique().drop("Record ID", axis=1).reset_index("Record ID")
    )
    counting_steps = Counter(counting_steps["Record ID"])
    return counting_steps


def set_equal_index_in_cycle(cycle):
    r = range(1, len(cycle) + 1)
    cycle.index = [i for i in r]
    return cycle


def check_on_rest(df: pd.DataFrame) -> bool:
    counting_steps = counting_record_id_in_cycle(df)
    if counting_steps["Rest"]:
        return True
    return False


def cut_needless_deltaes_value(deltaes: pd.DataFrame, n_step: int) -> pd.DataFrame:
    deltaes = deltaes.groupby("Cycle ID").head(n_step)
    return deltaes


def get_result(result: pd.Series) -> pd.DataFrame:
    result = result.groupby("Cycle ID").apply(set_equal_index_in_cycle)
    df = result.unstack("Cycle ID")
    return df


def cut_needless_rohm_value_only_dchg(rohm: pd.DataFrame) -> pd.DataFrame:
    rohm = rohm.iloc[3::2, :]
    rohm = set_equal_index_in_cycle(rohm)
    return rohm


def cut_needless_rohm_value(rohm: pd.DataFrame) -> pd.DataFrame:
    rohm = rohm.iloc[1::2, :]
    rohm = set_equal_index_in_cycle(rohm)
    return rohm


def cut_needless_rpol_value_only_dchg(
    rpol: pd.DataFrame, config_values: dict
) -> pd.DataFrame:
    rpol = rpol.iloc[1 : config_values["n_step"] + 1, :]
    rpol = set_equal_index_in_cycle(rpol)
    return rpol


def extract_voltage_if_only_dchg(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["Record ID"] != "CCCV_Chg"]
    voltage = df.groupby("Cycle ID").apply(set_equal_index_in_cycle)
    return voltage


def add_time_columns(voltage: pd.DataFrame) -> pd.DataFrame:
    voltage["time"] = (voltage.index - 1) * 60
    voltage["sqrttime"] = np.sqrt(voltage["time"])
    return voltage


def no_rest_voltage(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Record ID"] != "Rest"]


def get_sqrttime_voltage(voltage: pd.DataFrame) -> pd.DataFrame:
    sqrttime_voltage = no_rest_voltage(voltage)
    sqrttime_voltage = sqrttime_voltage.drop("time", axis=1)
    return sqrttime_voltage


def get_rohm(df: pd.DataFrame, config_values: dict) -> pd.DataFrame:
    rohm = calculate_rohm(df, config_values)
    if chg_equal_dchg(df):
        rohm = cut_needless_rohm_value(rohm)
        return rohm
    rohm = cut_needless_rohm_value_only_dchg(rohm)
    return rohm


def get_rpol(
    rest_df: pd.DataFrame, df: pd.DataFrame, config_values: dict
) -> pd.DataFrame:
    rpol = calculate_rpol(rest_df, config_values)
    if chg_equal_dchg(df):
        return rpol
    rpol = cut_needless_rpol_value_only_dchg(rpol, config_values)
    return rpol


def chg_equal_dchg(df: pd.DataFrame) -> bool:
    counting_steps = counting_record_id_in_cycle(df)
    return counting_steps["CC_DChg"] == counting_steps["CCCV_Chg"]


def get_rest_and_dchg_df(df: pd.DataFrame) -> tuple:
    rest_df = df[df["Record ID"] == "Rest"]
    dchg_df = dchg_equal_or_not(df)
    return (rest_df, dchg_df)


def get_d(
    rest_df: pd.DataFrame, dchg_df: pd.DataFrame, config_values: dict
) -> pd.DataFrame:
    deltaet = calculate_deltaet(dchg_df)
    deltaes = calculate_deltaes(rest_df)
    deltaes = cut_needless_deltaes_value(deltaes, config_values["n_step"])
    d = calculate_d(deltaet, deltaes, config_values)
    return d


def dchg_equal_or_not(df: pd.DataFrame) -> pd.DataFrame:
    if chg_equal_dchg(df):
        return df[df["Record ID"] != "Rest"]
    return df[df["Record ID"] == "CC_DChg"]


def get_capacity_div_mnav_col(df: pd.DataFrame, config_values: dict) -> pd.DataFrame:
    df["Cap/mnav"] = df["CmcCap(mAh/g)"] / config_values["mnav"]
    return df

def add_name_sample(df: pd.DataFrame, config_values: dict) -> pd.DataFrame:
    df["sample"] = config_values["sample"]
    df = df.reset_index()
    df = df.set_index(["sample", "Cycle ID"])
    return df


def get_result_formirovka(df: pd.DataFrame, config_values: dict) -> pd.DataFrame:
    df = get_capacity_div_mnav_col(df, config_values)
    qdchg = calculate_qdchg_formirovka(df)
    qchg_vol = calculate_qchg_vol_formirovka(df)
    result = pd.concat([qchg_vol, qdchg], axis=1)
    result.columns = ["Vol_end", "QChg", "QDch"]
    result = result.iloc[:-1, :]
    result = add_name_sample(result, config_values)
    return result


def get_all_results_gitt(df: pd.DataFrame, config_values: dict) -> list:

    rest_df, dchg_df = get_rest_and_dchg_df(df)
    d = get_d(rest_df, dchg_df, config_values)
    logd = d.apply(np.log10)
    rpol = get_rpol(rest_df, df, config_values)
    rohm = get_rohm(df, config_values)
    utitr = calculate_utitr(dchg_df)
    all_results = [d, logd, rpol, rohm, utitr]
    return all_results


def get_main_results_gitt(df: pd.DataFrame, config_values: dict) -> pd.DataFrame:
    all_results = get_all_results_gitt(df, config_values)
    result = pd.concat(all_results)
    result.index = set_index_names(df, config_values)
    return result

def set_index_names(df: pd.DataFrame, config_values: dict) -> list:
    names = ["D", "LogD", "Rpol", "Rohm", "U_титр"]
    if chg_equal_dchg(df):
        index = [
            f"{name}_{i}" for name in names for i in range(1, config_values["n_step"] * 2 + 1)
        ]
    else:
        index = [
            f"{name}_{i}" for name in names for i in range(1, config_values["n_step"] + 1)
        ]
    return index

        

def get_dict_with_all_results_gitt(file_path: str, config_values: dict) -> dict:
    df = get_data_general(file_path)
    df = find_gitt_cycle(df, config_values)
    result = get_main_results_gitt(df, config_values)
    voltage, norest_vol = get_voltage(df)
    dict_with_data = {"Result": result, "Voltage": voltage, "sqrttime": norest_vol}
    return dict_with_data


def drop_record_decorator(function):
    def drop_record_id(result):
        return result.reset_index(["Record ID", "Step ID"], drop=True)

    @functools.wraps(function)
    def wrapper(result):
        result = function(result)
        result = drop_record_id(result)
        return result

    return wrapper


def result_decorator(calculate_func):
    @functools.wraps(calculate_func)
    def transform_in_df(*args) -> pd.DataFrame:
        result = calculate_func(*args)
        df = get_result(result)
        return df

    return transform_in_df


def extract_voltage(df: pd.DataFrame) -> pd.Series:
    if chg_equal_dchg(df):
        voltage = df.groupby("Cycle ID").apply(set_equal_index_in_cycle)
        norest_vol = voltage[voltage["Record ID"] != "Rest"]
    else:
        voltage = extract_voltage_if_only_dchg(df)
        norest_vol = voltage[voltage["Record ID"] != "Rest"]
    return voltage, norest_vol


def get_voltage(df: pd.DataFrame) -> pd.DataFrame:
    voltage, norest_vol = extract_voltage(df)
    voltage = voltage["Voltage(V)"].unstack("Cycle ID")
    voltage = add_time_columns(voltage)
    norest_vol = norest_vol["Voltage(V)"].unstack("Cycle ID")
    norest_vol = add_time_columns(norest_vol)
    norest_vol = norest_vol.drop("time", axis=1)
    return voltage, norest_vol


def calc_D(d: pd.Series, config_values: dict) -> pd.Series:
    D = (4 / (math.pi * config_values["tau"])) * (
        np.square(
            (
                (config_values["m"] * config_values["V"])
                / (config_values["M"] * config_values["S"])
            )
        )
        * np.square(d)
    )
    return D


def calculate_deltaet(dchg_df: pd.DataFrame) -> pd.Series:
    voltage_groupby = dchg_df.groupby(["Cycle ID", "Step ID", "Record ID"])[
        "Voltage(V)"
    ]
    deltaet = abs(voltage_groupby.nth(1) - voltage_groupby.last())
    return deltaet


def calculate_deltaes(rest_df: pd.DataFrame) -> pd.Series:
    voltage_groupby = rest_df.groupby(["Cycle ID", "Step ID", "Record ID"])[
        "Voltage(V)"
    ]
    deltaes = abs(voltage_groupby.last() - voltage_groupby.last().shift(-1))
    return deltaes


@result_decorator
def calculate_rohm(df: pd.DataFrame, config_values: dict) -> pd.Series:
    voltage_groupby = df.groupby(["Cycle ID", "Step ID", "Record ID"])["Voltage(V)"]
    rohm = abs(voltage_groupby.last() - voltage_groupby.nth(1).values)
    rohm = rohm / config_values["I"]
    return rohm


@result_decorator
def calculate_rpol(rest_df: pd.DataFrame, config_values: dict) -> pd.Series:
    voltage_groupby = rest_df.groupby(["Cycle ID", "Step ID", "Record ID"])[
        "Voltage(V)"
    ]
    rpol = abs(voltage_groupby.last() - voltage_groupby.nth(1))
    rpol = rpol / config_values["I"]
    return rpol


@result_decorator
def calculate_utitr(dchg_df: pd.DataFrame) -> pd.Series:
    voltage_groupby = dchg_df.groupby(["Cycle ID", "Step ID", "Record ID"])[
        "Voltage(V)"
    ]
    utitr = voltage_groupby.last()
    return utitr


@result_decorator
def calculate_d(
    deltaet: pd.Series, deltaes: pd.Series, config_values: dict
) -> pd.Series:
    d = deltaes / deltaet.values
    D = calc_D(d, config_values)
    return D


def calculate_mean_if_rest(df: pd.DataFrame) -> pd.Series:
    groupby_df = df.shift(5).groupby(["Cycle ID", "Record ID"])["Voltage(V)"]
    mean_vol = groupby_df.mean()
    return mean_vol


def calculate_mean_no_rest(df: pd.DataFrame) -> pd.Series:
    groupby_df = df.groupby(["Cycle ID", "Record ID"])["Voltage(V)"]
    mean_vol = groupby_df.mean()
    return mean_vol


@drop_record_decorator
def calculate_qdchg_formirovka(df: pd.DataFrame) -> pd.Series:
    df = df[df["Record ID"] == "CC_DChg"]
    qdchg = df.groupby(["Cycle ID", "Step ID", "Record ID"])["Cap/mnav"].last()
    return qdchg


@drop_record_decorator
def calculate_qchg_vol_formirovka(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["Record ID"] == "CCCV_Chg"]
    vol_qchg = df.groupby(
        ["Cycle ID", "Step ID", "Record ID"])[["Voltage(V)", "Cap/mnav"]].last()
    return vol_qchg


