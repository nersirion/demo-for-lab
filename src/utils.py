from collections import Counter, namedtuple
import functools
import pandas as pd
import numpy as np

n_step = 4
def find_gitt_cycle(df): 
    return df.groupby('Cycle ID').filter(lambda x: counting_record_id_in_cycle(x)['CC_DChg']==n_step)
    
  
def counting_record_id_in_cycle(df):
    cycle_list = df['Cycle ID'].unique().astype(int)
    counting_steps=df[df['Cycle ID'] == cycle_list[0]].groupby(['Step ID', 'Record ID'])
    counting_steps = counting_steps.nunique().drop('Record ID', axis=1).reset_index('Record ID')
    counting_steps = Counter(counting_steps['Record ID'])
    return counting_steps

def set_equal_index_in_cycle(cycle):
    cyclce.index = [i for i in range(len(cycle))]
    return cycle

def cut_needless_deltaes_value(deltaet):
    deltaes = deltaes.groupby('Cycle ID').apply(lambda cycle: cycle.iloc[:n_step, :])
    return deltaes 

def get_result(resulst:pd.Series) -> pd.DataFrame:
    result = result.groupby('Cycle ID').apply(set_equal_index_in_cycle)
    df = result.groupby('Cycle ID').unstack('Cycle ID')
    return df


def cut_needless_rohm_value_only_dchg(df:pd.DataFrame) -> pd.DataFrame:
    return df.iloc[3::2, :]

def cut_needless_rohm_value(df:pd.DataFrame) -> pd.DataFrame:
    return df.iloc[1::2, :]
    
def extract_voltage_if_only_dchg(df:pd.DataFrame) -> pd.DataFrame:
    return df[df["Record ID"] != "CCCV_Chg"]

def add_time_columns(voltage:pd.DataFrame) -> pd.DataFrame:
    voltage['time'] = voltage.index * 60
    voltage['sqrttime'] = np.square(voltage['time'])
    return voltage

def no_rest_voltage(voltage: pd.DataFrame) -> pd.DataFrame:
    return voltage[voltage['Record ID'] != 'Rest']


def get_rohm(df:pd.DataFrame) -> pd.DataFrame:
    rohm = calculate_rohm(df)
    if chg_equal_dchg(df):
        rohm = cut_needless_rohm_value(df)
        return rohm
    rohm = cut_needless_rohm_value_only_dchg
    return rohm

def chg_equal_dchg(df:pd.DataFrame) -> bool:
    counting_steps = counting_record_id_in_cycle(df)
    return counting_steps['CC_DChg'] == counting_steps['CCCV_Chg']

def get_rest_and_dchg_df(df:pd.DataFrame) -> tuple:
    rest_df = df[df['Record ID'] == 'Rest']
    dchg_df = dchg_equal_or_not(df) 
    return (rest_df, dchg_df)

def get_d(rest_df: pd.DataFrame, dchg_df:pd.DataFrame) -> pd.DataFrame:
    deltaet = calculate_deltaet(dchg_df)
    deltaes = calculate_deltaes(rest_df)
    deltaes = cut_needless_deltaet_value(deltaes)
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
    rpol = calculate_rpol(rest_df)
    rohm = get_rohm(df)
    utitr = calculate_utitr(dchg_df)
    all_results = [d, logd, rpol, rohm, utitr]
    return all_results 

def get_final_results_gitt(df:pd.DataFrame) -> pd.DataFrame:
    all_results = get_all_results_gitt(df)
    result = pd.concat(all_results)
    names = ['D', 'LogD', 'Rpol', 'Rohm', 'U_титр']
    result.index = [f'{name}_{i}' for name in names for i in range(1,n_step)]
    return result


def check_on_rest(df:pd.DataFrame) -> bool:
    counting_steps = counting_record_id_in_cycle(df)
    if counting_steps["Rest"]:
        return True
    return False

