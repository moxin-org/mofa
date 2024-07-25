import pandas as pd
import yaml
def read_yaml(file_path:str):
    with open(file_path, 'r') as file:
        prime_service = yaml.safe_load(file)
    return prime_service

def read_text(file_path: str = '/mnt/d/project/dy/extra/nlp/uie/The Three-Body Problem 1: The Madness Years.txt',encoding:str='utf-8') -> str:
    content = ""
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
    return content




def read_excel(file_path:str, sheet_names:list[str]=None)->[dict]:
    """
    Read all sheets or specified sheets from an Excel file and generate a list of dictionaries.

    Parameters:
    file_path (str): Path to the Excel file.
    sheet_names (list, optional): List of sheet names to read. If not provided, all sheets will be read.

    Returns:
    list: A list of dictionaries, each containing the data from a sheet. Each dictionary's key is the sheet name, and the value is the content (DataFrame) of that sheet.
    """

    xls = pd.ExcelFile(file_path)
    all_sheet_names = xls.sheet_names

    if sheet_names is None:
        sheet_names = all_sheet_names

    invalid_sheets = [sheet for sheet in sheet_names if sheet not in all_sheet_names]
    if invalid_sheets:
        raise ValueError(f"The following sheets are not found in the Excel file: {', '.join(invalid_sheets)}")
    sheets_data = []
    for sheet_name in sheet_names:
        sheet_df = pd.read_excel(file_path, sheet_name=sheet_name)
        sheets_data.append({sheet_name: sheet_df})

    return sheets_data