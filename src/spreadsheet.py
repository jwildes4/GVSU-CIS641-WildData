import pandas as pd


def read_spreadsheet(file):
    df = pd.read_excel(file, sheet_name=0)

    if df.empty:
        raise ValueError("The spreadsheet is empty.")

    return df
