import pandas as pd


def find_gitt_cycle(df):
    return df = df.groupby('Cycle ID').filter(lambda x: len(x[x['Record ID'] == 'CC_DChg'])==n_step)
    
  
def counting_steps_in_gitt_cycle(df):
    cycle_list = df['Cycle ID'].unique().astype(int)
    counting_steps=df[df['Cycle ID'] == cycle_list[0]].groupby(['Step ID', 'Record ID'])
    counting_steps = counting_steps.nunique().drop('Record ID', axis=1).reset_index('Record ID')
    counting_steps = Counter(counting_steps['Record ID'])
    return counting_steps
    
def transform_data_when_chg_equal_dchg(cycle_df):
    vol+=step_df.iloc[1:-1].tolist()
    if i[1] == 'Rest':
        rest.append(step.iloc[-1, -1])
        r1.append(abs(step.iloc[2,-1] - u))
        r2.append(abs(step.iloc[-1, -1] - step.iloc[2,-1]))
    elif i[1] == 'CC_DChg':
        dchg.append(abs(step.iloc[2, -1] - step.iloc[-1, -1]))
        u = step.iloc[-1, -1]
        u_dchg.append(u)
    else:
        chg.append(abs(step.iloc[2, -1] - step.iloc[-1, -1]))
        u = step.iloc[-1, -1]
        u_chg.append(u)
