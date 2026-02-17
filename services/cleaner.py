import pandas as pd
import numpy as np
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

    return file

def clean(file):

    file = removeDuplicates(file)

    file["date_de_vente"] = standardizeDates(file["date_de_vente"])
    file["montant"] = normalizePrices(file["montant"])
    file["telephone"] = standardizePhoneNumbers(file["telephone"])
    file["nom"] = standardizeNames(file["nom"])

    file = cleanColumns(file)

    return file

def merge(file1,file2):

    file = mergesFiles(file1,file2)

    return file

def normalizePrices(columnName,devise) :
    
    """
    This function normalize prices.

    Input :
        - Column with prices
        - Devise of money

    Output :
        - Column with normalized prices
    """
    
    columnName = columnName.astype(str)
    columnName = columnName.str.replace(r'[€$]', f'{devise}', regex=False)
    columnName = columnName.str.replace(',', '.', regex=False)
    columnName = columnName.str.strip()
    columnName = pd.to_numeric(columnName, errors='coerce')
    
    return columnName

def standardizeDates(column,dayFirst) :

    """
    This function normalize prices in format YYYY-MM-DD or DD-MM-YYYY.

    Input :
        - Column with dates
        - Day Fisrt (bool) : True for french format

    Output :
        - Column with standadized dates
    """

    standardizedDates = []

    for val in column :
        
        if pd.isna(val) :
           standardizedDates.append(pd.NaT)
        
        try :
            parsedDate = parser.parse(str(val), dayfirst=dayFirst)
            standardizedDates.append(parsedDate.strftime("%Y-%M-%D"))

        except :
            standardizedDates.append(pd.NaT)

    return pd.Series(standardizedDates)

def standardizePhoneNumbers(column, defaultCountryCode) :

    """
    This function normalize phone number.

    Input :
        - Column with phone number
        - defaultCountryCode : default country code if missing (e.g., '+33')

    Output :
        - Column with standadized phone number
    """

    standardizedPhoneNumbers = []
    
    for value in column :

        if pd.isna(value) :
            standardizedPhoneNumbers.append(None)
            continue

        value = str(value).strip()
        digits = re.sub(r'[^0-9+]', '', value)

        if digits.startswith("00") :
            digits = "+" + digits[2:]

        elif digits.startswith("0") :
            digits = defaultCountryCode + digits[1:]

        if len(digits) < 7 :
            standardizedPhoneNumbers.append(None)

        else :
            standardizedPhoneNumbers.append(digits)
    
    return pd.Series(standardizedPhoneNumbers)

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

def deleteRow(columnName,file):

    """
    This function can detelete a targeted empty row.

    Entry :
        - ColumnName : Name of the column we want to detelete if nothing in it

    Output :
        - File : the dictionnary without the empties columns
    """

    file = file.to_dict(orient='list')
    attempt = file[columnName].count(np.nan)

    for _ in range(attempt) :
        index = file[columnName].index(np.nan)

        for key in file.keys():
            file[key].pop(index)

    return file