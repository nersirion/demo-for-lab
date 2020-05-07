from collections import Counter, namedtuple
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
    
def transform_data_when_chg_equal_dchg(cycle_df, result):
    rest = abs(cycle_df.iloc[0, -1] - temporary_data['rest'][0]) +\
    list(abs(np.array(temporary_data['rest'][:-1]) - np.array(temporary_data['rest'][1:])))
    result['vol'].append(cycle_df.loc[:, ['Record ID', 'Step ID', 'Voltage(v)']])
    result['DeltaEt'].append(temporary_data['chg'] + temporary_data['dchg'])
    result['DeltaEs'].append(rest)
    result['U'].append(temporary_data['u_chg'] + temporary_data['u_dchg'])
    result['Rohm'].append(r1)
    result['Rpol'].apppend(r2)

    return result

def transform_data_when_chg_not_equal_dchg(result, temporary_data):
    rest = list(abs(np.array(temporary_data['rest'][:n_step]) - np.array(temporary_data['rest'][1:n_step+1])))
    #result['Voltage'].append(cycle_df.loc[:, ['Record ID', 'Step ID', 'Voltage(v)']])
    result['DeltaEt'].append(temporary_data['dchg'])
    result['DeltaEs'].append(rest)
    result['U'].append(temporary_data['u_dchg'])
    result['Rohm'].append(temporary_data['r1'][1:n_step+1])
    result['Rpol'].append(temporary_data['r2'][1:n_step+1])

    return result


def extract_temporary_data(step_df, temporary_data):
   if step_df['Record ID'].iloc[0] == 'Rest':
        temporary_data['rest'].append(step_df.iloc[-1, -1])
        temporary_data['r1'].append(abs(step_df.iloc[1,-1] - temporary_data['u']))
        temporary_data['r2'].append(abs(step_df.iloc[-1, -1] - step_df.iloc[1,-1]))
   elif step_df['Record ID'].iloc[0] == 'CC_DChg':
        temporary_data['dchg'].append(abs(step_df.iloc[1, -1] - step_df.iloc[-1, -1]))
        temporary_data['u'] = step_df.iloc[-1, -1]
        temporary_data['u_dchg'].append(temporary_data['u'])
   else:
        temporary_data['chg'].append(abs(step_df.iloc[1, -1] - step_df.iloc[-1, -1]))
        temporary_data['u'] = step_df.iloc[-1, -1]
        temporary_data['u_chg'].append(temporary_data['u'])
   return temporary_data


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
