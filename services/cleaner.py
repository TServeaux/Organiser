import pandas as pd
from dateutil import parser
import re
import os
import json

def getDataFromSheet(file) :

    """
    This function transform the excel file into a matrix of data.

    Input :
        - File (excel or csv)

    Output :
        - Matrix of data -> pd.DataFrame
    """
    
    fileType = os.path.splitext(file)[1] # determine the type of the file
    
    if fileType == ".xlsx" :
        file = pd.read_excel(file)

    elif fileType == ".csv" :
        file = pd.read_csv(file)

    else : 
        return "Not good type of file"

    file.rename(columns=str.lower, inplace=True)

    return file,fileType

def clean(file,outputPath):
    """
    This function apply the algorithm of cleaning.
    """

    file,fileType = getDataFromSheet(file)
    data = readParameter("./config.json")

    file = cleanColumns(file)

    subset = data['duplicates']['subset']
    if not subset or subset == "None":
        subset = None

    file = removeDuplicates(file,subset=subset,keep=data['duplicates']['keep'])

    col = data["dates"]["columnName"]
    file[col] = standardizeDates(file[col], data["dates"]["dayFirst"])

    col = data["prices"]["columnName"]
    file[col] = normalizePrices(file[col])

    col = data["phone"]["columnName"]
    file[col] = standardizePhoneNumbers(file[col] ,data["phone"]["defaultCountryCode"])

    col = data["names"]["columnName"]
    file[col] = standardizeNames(file[col])

    if outputPath.lower().endswith(".xlsx"):
        file.to_excel(outputPath, index=False)

    else:
        file.to_csv(outputPath, index=False)

    return file

def merge(file1, file2, outputPath):

    file1, _ = getDataFromSheet(file1)
    file2, _ = getDataFromSheet(file2)

    config = readParameter("./config.json")
    merge_cfg = config.get("merge", {})

    on = merge_cfg.get("on")
    how = merge_cfg.get("how", "inner")

    if on == "None" or on == []:
        on = None

    merged = mergesFiles(file1, file2, on=on, how=how)

    if outputPath.lower().endswith(".xlsx"):
        merged.to_excel(outputPath, index=False)
    else:
        merged.to_csv(outputPath, index=False)

    return merged

def normalizePrices(columnName) :
    
    """
    This function normalize prices.

    Input :
        - Column with prices
        - Devise of money

    Output :
        - Column with normalized prices
    """
    
    columnName = columnName.astype(str)
    columnName = columnName.str.replace(r'[€$]', '', regex=True)
    columnName = columnName.str.replace(r'\s+', '', regex=True)
    columnName = columnName.str.replace(',', '.', regex=False)
    columnName = pd.to_numeric(columnName, errors='coerce')
    
    return columnName

def standardizeDates(column, dayFirst):
    """
    Standardizes dates to YYYY-MM-DD.

    Input:
        - column: pandas Series containing dates

    Output:
        - pandas Series of standardized dates (datetime64)
    """

    def smart_parse_date(value):
        if pd.isna(value):
            return pd.NaT

        value = str(value).strip()

        try:
            return parser.parse(value, dayfirst=True, fuzzy=True)
        except Exception:
            return pd.NaT

    return column.apply(smart_parse_date)

def standardizePhoneNumbers(column, defaultCountryCode) :

    """
    This function normalize phone number.

    Input :
        - Column with phone number
        - defaultCountryCode : default country code if missing (e.g., '+33')

    Output :
        - Column with standadized phone number
    """

    result = []

    for value in column:
        if pd.isna(value):
            result.append(None)
            continue

        value = str(value).strip()
        digits = re.sub(r'[^0-9+]', '', value)

        if digits.startswith("00"):
            digits = "+" + digits[2:]

        elif digits.startswith(defaultCountryCode.replace("+", "")):
            digits = "+" + digits

        elif digits.startswith("0"):
            digits = defaultCountryCode + digits[1:]

        if len(re.sub(r'\D', '', digits)) < 10:
            result.append(None)
        else:
            result.append(digits)

    return pd.Series(result, index=column.index)

def standardizeNames(column):

    """
    This function standardize names.

    Input :
        - Column of names

    Output :
        - Column of standardized names
    """
    
    column = column.str.strip()
    column = column.str.replace(r'\s+', ' ', regex = True)
    column = column.str.title()

    return column

def removeDuplicates(file , subset, keep) :
    """
    Delete doublon in a file.

    Input :
        - File to clean
        - Subset : list or None → column to verifie for doublons (None = toutes les colonnes)
        - Keep : 'first', 'last', False for which you want to keep ('first' = first occurence)

    Output :
        - File cleaned, without doublons
    """

    cleanedFile = file.drop_duplicates(subset=subset, keep=keep)
    return cleanedFile

def mergesFiles(file1,file2,on,how):
    """
    Merges two DataFrames into a single DataFrame.

    Input:
        - file1 : The second file to merge.
        - file2 : The second file to merge.
        - On : list (optional).
        Column(s) to join on. If None, merges on columns with the same names.
        - How : str, default 'inner'
            Type of merge to perform:
                - 'left' : All rows from the left DataFrame + matching rows from the right
                - 'right': All rows from the right DataFrame + matching rows from the left
                - 'outer': All rows from both DataFrames
                - 'inner': Only rows that exist in both DataFrames

    Output:
        -A new file resulting from merging file1 and file2.
    """
    
    mergedFile = pd.merge(file1, file2, on=on, how=how)
    
    return mergedFile


def cleanColumns(file):
    """
    Standardizes column names:
        - Converts to lowercase
        - Replaces spaces with '_'
        - Removes special characters
        - Strips leading and trailing spaces
    """

    cleanedColumns = []

    for column in file.columns:

        newColumn = str(column).lower().strip()
        newColumn = re.sub(r'[\s\-]+', '_', newColumn)
        newColumn = re.sub(r'[^\w_]', '', newColumn)

        cleanedColumns.append(newColumn)

    file.columns = cleanedColumns
    
    return file

def readParameter(data) :
    
    with open(data,'r',encoding='utf-8') as d:
        data = json.load(d)
    
    return data