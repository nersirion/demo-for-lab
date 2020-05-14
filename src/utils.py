from collections import Counter
import functools
import math
import pandas as pd
import numpy as np
from get_data import *


def find_gitt_cycle(df): 
    return df.groupby('Cycle ID').filter(lambda x: counting_steps_in_gitt_cycle(x)['CC_DChg']==n_step)
  
def counting_steps_in_gitt_cycle(df):
    cycle_list = df['Cycle ID'].unique().astype(int)
    counting_steps=df[df['Cycle ID'] == cycle_list[0]].groupby(['Step ID', 'Record ID'])
    counting_steps = counting_steps.nunique().drop('Record ID', axis=1).reset_index('Record ID')
    counting_steps = Counter(counting_steps['Record ID'])
    return counting_steps

def set_equal_index_in_cycle(cycle):
    r = range(1, len(cycle)+1)
    cycle.index = [i for i in r]
    return cycle

def cut_needless_deltaes_value(deltaes):
    deltaes = deltaes.groupby('Cycle ID').head(n_step)
    return deltaes 

def get_result(result:pd.Series) -> pd.DataFrame:
    result = result.groupby('Cycle ID').apply(set_equal_index_in_cycle)
    df = result.unstack('Cycle ID')
    return df

def cut_needless_rohm_value_only_dchg(rohm:pd.DataFrame) -> pd.DataFrame:
    rohm = rohm.iloc[3::2, :]
    rohm = set_equal_index_in_cycle(rohm)
    return rohm

def cut_needless_rohm_value(rohm:pd.DataFrame) -> pd.DataFrame:
    rohm = rohm.iloc[1::2, :]
    rohm = set_equal_index_in_cycle(rohm)
    return rohm
    
def cut_needless_rpol_value_only_dchg(rpol:pd.DataFrame) -> pd.DataFrame:
    rpol = rpol.iloc[1:n_step+1, :]
    rpol = set_equal_index_in_cycle(rpol)
    return rpol

def extract_voltage_if_only_dchg(df:pd.DataFrame) -> pd.DataFrame:
    return df[df["Record ID"] != "CCCV_Chg"]

def add_time_columns(voltage:pd.DataFrame) -> pd.DataFrame:
    voltage['time'] = voltage.index * 60
    voltage['sqrttime'] = np.square(voltage['time'])
    return voltage

def no_rest_voltage(voltage: pd.DataFrame) -> pd.DataFrame:
    return voltage[voltage['Record ID'] != 'Rest']


def get_voltage(df:pd.DataFrame) -> pd.DataFrame:
    if chg_equal_dchg(df):
       voltage = df
    else:
        voltage = extract_voltage_if_only_dchg(df)
    voltage = add_time_columns(voltage)
    return voltage

def get_sqrttime_voltage(voltage: pd.DataFrame) -> pd.DataFrame:
    sqrttime_voltage = no_rest_voltage(voltage)
    sqrttime_voltage = sqrttime_voltage.drop("time", axis=1)
    return sqrttime_voltage

def get_rohm(df:pd.DataFrame) -> pd.DataFrame:
    rohm = calculate_rohm(df)
    if chg_equal_dchg(df):
        rohm = cut_needless_rohm_value(rohm)
        return rohm
    rohm = cut_needless_rohm_value_only_dchg(rohm)
    return rohm

def get_rpol(rest_df, df):
    rpol = calculate_rpol(rest_df)
    if chg_equal_dchg(df):
        return rpol
    rpol = cut_needless_rpol_value_only_dchg(rpol)
    return rpol

def chg_equal_dchg(df:pd.DataFrame) -> bool:
    counting_steps = counting_steps_in_gitt_cycle(df)
    return counting_steps['CC_DChg'] == counting_steps['CCCV_Chg']

def get_rest_and_dchg_df(df:pd.DataFrame) -> tuple:
    rest_df = df[df['Record ID'] == 'Rest']
    dchg_df = dchg_equal_or_not(df) 
    return (rest_df, dchg_df)

def get_d(rest_df: pd.DataFrame, dchg_df:pd.DataFrame) -> pd.DataFrame:
    deltaet = calculate_deltaet(dchg_df)
    deltaes = calculate_deltaes(rest_df)
    deltaes = cut_needless_deltaes_value(deltaes)
    d = calculate_d(deltaet, deltaes)
    return d

def dchg_equal_or_not(df:pd.DataFrame) -> pd.DataFrame:
    if chg_equal_dchg(df):
        return df[df['Record ID'] !='Rest']
    return df[df['Record ID'] == 'CC_DChg']

    
def get_capacity_div_mnav_col(df:pd.DataFrame) -> pd.DataFrame:
    df['Cap/mnav'] = df['CmcCap(mAh/g)'] / mnav
    return df

def get_result_formirovka(df:pd.DataFrame) -> pd.DataFrame:
    qdchg = calculate_qch_formirovka(df)
    vol_qchg = calculate_qdch_vol_formirovka(df)
    result = pd.concat([qdch_vol, qch], axis=1)
    result.columns = ['Vol_end', 'QChg', 'QDch']
    return result

def get_all_results_gitt(df: pd.DataFrame) -> list:

    rest_df, dchg_df = get_rest_and_dchg_df(df)
    d = get_d(rest_df, dchg_df)
    logd = d.apply(np.log10)
    rpol = get_rpol(rest_df, df)
    rohm = get_rohm(df)
    utitr = calculate_utitr(dchg_df)
    all_results = [d, logd, rpol, rohm, utitr]
    return all_results 

def get_main_results_gitt(df:pd.DataFrame) -> pd.DataFrame:
    all_results = get_all_results_gitt(df)
    result = pd.concat(all_results)
    names = ['D', 'LogD', 'Rpol', 'Rohm', 'U_титр']
    result.index = [f'{name}_{i}' for name in names for i in range(1,n_step+1)]
    return result

def get_dict_with_all_results_gitt(file_path:str) -> dict:
    df = get_data_general(file_path)
    df = find_gitt_cycle(df)
    result = get_main_results_gitt(df)
    voltage = get_voltage(df)
    sqrttime_voltage = get_sqrttime_voltage(voltage)
    dict_with_data = {"Result": result,
                      "Voltage": voltage,
                      "sqrttime": sqrttime_voltage}
    return dict_with_data

                            
def drop_record_decorator(function):
    def drop_record_id(result):
        return result.reset_index('Record ID', drop=True)
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

def calc_D(d:pd.Series) -> pd.Series:
    D = (4/(math.pi*tau))*(np.square(((m*V)/(M*S)))*np.square(d))   
    return D

def calculate_deltaet(dchg_df: pd.DataFrame) -> pd.Series:
    voltage_groupby = dchg_df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    deltaet = abs(voltage_groupby.nth(1) - voltage_groupby.last())
    return deltaet

def calculate_deltaes(rest_df: pd.DataFrame) -> pd.Series:
    voltage_groupby = rest_df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    deltaes = abs(voltage_groupby.last() - voltage_groupby.last().shift(-1))
    return deltaes

@result_decorator
def calculate_rohm(df:pd.DataFrame) -> pd.Series:
    voltage_groupby = df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    rohm = abs(voltage_groupby.last() - voltage_groupby.nth(1).values)
    rohm = rohm / I
    return rohm

@result_decorator
def calculate_rpol(rest_df: pd.DataFrame) -> pd.Series:
    voltage_groupby =  rest_df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    rpol = abs(voltage_groupby.last() - voltage_groupby.nth(1))
    rpol = rpol / I
    return rpol

@result_decorator
def calculate_utitr(dchg_df: pd.DataFrame) -> pd.Series:
    voltage_groupby =  dchg_df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    utitr = voltage_groupby.last()
    return utitr

@result_decorator
def calculate_d(deltaet:pd.Series, deltaes:pd.Series) -> pd.Series:
    d = deltaes/deltaet.values
    D = calc_D(d)
    return D


def calculate_mean_if_rest(df:pd.DataFrame) -> pd.Series:
    groupby_df = df.shift(5).groupby(['Cycle ID', 'Record ID'])['Voltage(V)']
    mean_vol = groupby_df.mean()
    return mean_vol

def calculate_mean_no_rest(df:pd.DataFrame) -> pd.Series:
    groupby_df = df.groupby(['Cycle ID', 'Record ID'])['Voltage(V)']
    mean_vol = groupby_df.mean()
    return mean_vol

@drop_record_decorator
def calculate_qdchg_formirovka(df:pd.DataFrame) -> pd.Series:
    df = df[df['Record ID'] == 'CCCV_Chg']
    qdchg=df.groupby(['Cycle ID', 'Step ID', 'Record ID']['Cap/mnav']).last()
    return qdchg

@drop_record_decorator
def calculate_vol_qchg_formirovka(df:pd.DataFrame) -> pd.DataFrame:
    df = df[df['Record ID'] == 'CC_DChg']
    vol_qchg=df.groupby(['Cycle ID', 'Step ID', 'Record ID'][['Voltage(V)', 'Cap/mnav']]).last()
    return vol_qchg





