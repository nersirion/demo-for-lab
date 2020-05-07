from collections import Counter, namedtuple
import functools
import pandas as pd
import numpy as np

n_step = 4
def find_gitt_cycle(df): 
    return df.groupby('Cycle ID').filter(lambda x: counting_steps_in_gitt_cycle(x)['CC_DChg']==n_step)
    
  
def counting_steps_in_gitt_cycle(df):
    cycle_list = df['Cycle ID'].unique().astype(int)
    counting_steps=df[df['Cycle ID'] == cycle_list[0]].groupby(['Step ID', 'Record ID'])
    counting_steps = counting_steps.nunique().drop('Record ID', axis=1).reset_index('Record ID')
    counting_steps = Counter(counting_steps['Record ID'])
    return counting_steps

def filter_for_deltaet(record_id) -> bool:
    return bool(record_id['Record ID'].unique() == ['CC_DCchg'])


def filter_for_deltaes(record_id) -> bool:
    return bool(record_id['Record ID'].unique() == ['Rest'])

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

def result_decorator(calculate_func):
    @functools.wraps(calculate_func)
    def wrapper(result:pd.Series) -> pd.DataFrame:
        result =calculate_func(result)
        df = get_result(result)
        return df
    return wrapper

def cut_needless_rohm_value_only_dchg(df:pd.DataFrame) -> pd.DataFrame:
    return df.iloc[3::2, :]

def cut_needless_rohm_value(df):
    return df.iloc[1::2, :]
    
def extract_voltage_if_only_dchg(df:pd.DataFrame):


def add_time_columns(voltage):
    voltage['time'] = voltage.index * 60
    voltage['sqrttime'] = np.square(voltage['time'])
    return voltage

def no_rest_voltage(voltage: pd.DataFrame) -> pd.DataFrame:
    return voltage[voltage['Record ID'] != 'Rest']

def get_final_result(df: pd.DataFrame) -> pd.DataFrame:

    rest_df, dchg_df = get_rest_and_dchg_df(df)
    d = get_d(rest_df, dchg_df)
    rpol = calculate_rpol(rest_df)
    rohm = calculate_rohm(df)
    rohm = cut_needless_rohm_value_only_dchg(rohm)

    utitr = calculate_utitr(dchg_df)
    result = 

def get_rest_and_dchg_df(df:pd.DataFrame) -> tuple:
    rest_df = df[df['Record ID'] == 'Rest']
    dchg_df = df[df['Record ID'] != 'Rest']
    return (rest_df, dchg_df)

def get_d(rest_df: pd.DataFrame, dchg_df:pd.DataFrame) -> pd.DataFrame:
    deltaet = calculate_deltaet(dchg_df)
    deltaes = calculate_deltaes(rest_df)
    deltaes = cut_needless_deltaet_value(deltaes)
    d = calculate_d(deltaet, deltaes)
    return d




def extract_voltage


def create_df(result):
  for name, data in result.items():
      if name != 'cycle_list':
         result[name] = pd.DataFrame(data).T
	 #result[name].columns = ['{}_{}'.format(name,c) for c in range(1,5)]
  return result

def add_D_df(result):
   result['D'] = pd.DataFrame(result['DeltaEs'].values/result['DeltaEt'].values)
   result['logD'] = result['D'].apply(np.log10)
   return result


def concatenate_data_in_final_df(result):
    Result = pd.concat([
   		result['D'],
		result['logD'],
		result['Rohm'],
		result['Rpol'],
		result['U']
	])

    return Result
