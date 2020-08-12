import os
import pandas as pd
import config


def get_data_general(file_path):
    dfs = pd.read_excel(file_path, usecols=[0, 1, 2, 4, 8], header=2, sheet_name=None)
    df = pd.concat(dfs[sheet] for sheet in dfs.keys())
    df.columns = ["Cycle ID", "Step ID", "Record ID", "Voltage(V)", "CmcCap(mAh/g)"]
    df = df.ffill()
    if df["Voltage(V)"].mean() > 1000:
        df["Voltage(V)"] = df["Voltage(V)"] / 1000
    df["Record ID"] = df["Record ID"].str.replace("\d+", "")
    df = df.groupby("Cycle ID").ffill().dropna()
    df = (
        df.groupby(["Step ID", "Record ID"])
        .apply(lambda group: group.iloc[1:, :])
        .reset_index(drop=True)
    )
    df.iloc[:, -2] = correcting_result(df.iloc[:, -2])
    df.iloc[:, -1] = correcting_result(df.iloc[:, -1])
    return df


def get_data_custom(file_path):
    df = pd.DataFrame()
    dfs_on_sheets = pd.read_excel(file_path, sheet_name=None)
    for sheet, df_on_sheet in dfs_on_sheets.items():
        if 'record' not in sheet:
            continue
        if df_on_sheet.iloc[0, 0] == "Cycle ID":
            df_on_sheet.columns = df_on_sheet.iloc[0]
            df_on_sheet = df_on_sheet.drop(0)
        if 'Temperature(°C)' in str(df_on_sheet.columns[:8]):
            df_on_sheet = df_on_sheet.iloc[:, [0, 1, 2, 5, 8]]
        else:
            df_on_sheet = df_on_sheet.iloc[:, [0, 1, 2, 5, 7]]
        df_on_sheet.columns = ["Cycle ID", "Step ID", "Record ID", "Voltage(V)", "CmcCap(mAh/g)"]
        df_on_sheet = df_on_sheet.astype(
            {"Cycle ID": "float", "Step ID": "float", "Voltage(V)": "float"}
        )
        df_on_sheet["Record ID"] = df_on_sheet["Record ID"].str.replace("\t", "")
        if df_on_sheet["Voltage(V)"].mean() > 1000:
            df["Voltage(V)"] = df["Voltage(V)"] / 1000
        df = pd.concat([df_on_sheet, df])
    df.iloc[:, -2] = correcting_result(df.iloc[:, -2])
    df.iloc[:, -1] = correcting_result(df.iloc[:, -1])
    return df


def get_df(file_path: str) -> pd.DataFrame:
    if 'custom' in file_path:
        return get_data_custom(file_path)
    return get_data_general(file_path)


def get_data_for_calculate(path: str) -> pd.DataFrame:
    path = f"{path}/config/config.xlsx"
    df = pd.read_excel(path, index_col=0)
    return df

def correcting_result(column: pd.Series) -> pd.Series:
    num = len(str(int(250/column.mean())))-1
    column = column * 10**num
    return column
