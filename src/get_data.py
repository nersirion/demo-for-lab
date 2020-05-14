import os
import pandas as pd
import config

def get_data_general(file_path):
    dfs = pd.read_excel(file_path, usecols=[0,1,2,4,8], header=2, sheet_name=None)
    df = pd.concat(dfs[sheet] for sheet in dfs.keys())
    df.columns = ['Cycle ID', 'Step ID', 'Record ID', 'Voltage(V)', 'CmpCap(mAh/g)']
    df = df.ffill()
    if df['Voltage(V)'].mean()>1000:
        df['Voltage(V)'] = df['Voltage(V)']/1000
    df['Record ID'] = df['Record ID'].str.replace('\d+', '')
    df = df.groupby('Cycle ID').ffill().dropna()
    df = df.groupby(['Step ID', 'Record ID']).apply(lambda group: group.iloc[1:, :]).reset_index(drop=True)
    return df



def get_data_custom(file_path, sheets_list):
    df = pd.DataFrame()
    for sheet in sheets_list:
        try:
            df_on_sheet = pd.read_excel(file_path, sheet_name=sheet)
            if df_on_sheet.iloc[0, 0] == 'Cycle ID':
                df_on_sheet.columns = df_on_sheet.iloc[0]
                df_on_sheet = df_on_sheet.drop(0)
        except:
            continue
        df_on_sheet = df_on_sheet.iloc[:, [0,1, 2, 5]]
        df_on_sheet.columns = ['Cycle ID','Step ID', 'Step Name',  'Voltage(V)']
        df_on_sheet = df_on_sheet.astype({'Cycle ID': 'float', 'Step ID': 'float', 'Voltage(V)':'float'})
        df_on_sheet['Step Name']=df_on_sheet['Step Name'].str.replace('\t', '')
        if df_on_sheet['Voltage(V)'].mean()>1000:
            df['Voltage(V)'] = df['Voltage(V)']/1000
        df = pd.concat([df_on_sheet, df])
    return df

def get_data_for_calculate() -> pd.DataFrame:
    path = f'{config.PATH}/config/config.xlsx'
    df = pd.read_excel(path, index_col=0)
    return df



