from collections import Counter, namedtuple
import pandas as pd

n_step = 4
def find_gitt_cycle(df):
    return df.groupby('Cycle ID').filter(lambda x: counting_steps_in_gitt_cycle(x)['CC_DChg']==n_step)
    
  
def counting_steps_in_gitt_cycle(df):
    cycle_list = df['Cycle ID'].unique().astype(int)
    counting_steps=df[df['Cycle ID'] == cycle_list[0]].groupby(['Step ID', 'Record ID'])
    counting_steps = counting_steps.nunique().drop('Record ID', axis=1).reset_index('Record ID')
    counting_steps = Counter(counting_steps['Record ID'])
    return counting_steps
    
def transform_data_when_chg_equal_dchg(cycle_df, result):
    result.vol.extend(cycle_df.iloc[:,-1].tolist())
    if cycle_df['Record ID'].iloc[0] == 'Rest':
        result.rest.append(cycle_df.iloc[-1, -1])
        result.r1.append(abs(cycle_df.iloc[1,-1] - u))
        result.r2.append(abs(cycle_df.iloc[-1, -1] - cycle_df.iloc[1,-1]))
    elif cycle_df['Record ID'].iloc[0] == 'CC_DChg':
	result.vol_without_rest.extend(cycle_df.iloc[:,-1].tolist())
        result.dchg.append(abs(cycle_df.iloc[1, -1] - cycle_df.iloc[-1, -1]))
        result.u = cycle_df.iloc[-1, -1]
        result.u_dchg.append(result.u)
    else:
        result.vol_without_rest.extend(cycle_df.iloc[:,-1].tolist())
        result.chg.append(abs(cycle_df.iloc[1, -1] - cycle_df.iloc[-1, -1]))
        result.u = cycle_df.iloc[-1, -1]
        result.u_chg.append(result.u)
    
    return result
