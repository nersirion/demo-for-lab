import pandas as pd


def calc_D(d:pd.Series) -> pd.Series:
    D = (4/(math.pi*kwargs['tau']))*(np.square(((kwargs['m']*kwargs['V'])/(kwargs['M']*kwargs['S'])))*np.square(divDelta))    
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
def calculate_rohm(df: pd.DataFrame) ->pd.Series:
    voltage_groupby = df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    rohm = abs(voltage_groupby.last() - voltage_groupby.nth(1).shift(1))
    return rohm

@result_decorator
def calculate_rpol(rest_df: pd.DataFrame) -> pd.Series:
    voltage_groupby =  df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    rpol = abs(voltage_groupby.last() - voltage_groupby.nth(1))
    return rpol

@result_decorator
def calculate_utitr(dchg_df: pd.DataFrame) -> pd.Series:
    voltage_groupby =  df.groupby(['Cycle ID', 'Step ID', 'Record ID'])['Voltage(V)']
    utitr = voltage_groupby.last()
    return utitr

@result_decorator
def calculate_d(deltaet:pd.Series, deltaes:pd.Series) -> pd.Series:
    d = deltaes/deltaet
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
    df = df[df['Record ID'] == 'DCC_Chg']
    qdchg=df.groupby(['Cycle ID', 'Step ID', 'Record ID']['Cap/mnav'].last()
    return qdchg

@drop_record_decorator
def calculate_vol_qchg_formirovka(df:pd.DataFrame) -> pd.DataFrame:
    df = df[df['Record ID'] == 'CC_DChg']
    vol_qchg=df.groupby(['Cycle ID', 'Step ID', 'Record ID'][['Voltage(V)', 'Cap/mnav']].last()
    return vol_qchg


