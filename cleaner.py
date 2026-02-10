import pandas as pd
import numpy as np
import os

def getDataFromSheet(file):

    """
    This function transform the excel file into a matrix of data.
    Entry :
        - File (excel or csv)
    Output :
        - Matrix of data (dictionnary)
    """
    
    fileType = os.path.splitext(file)[1] # determine the type of the file
    
    if fileType == ".xlsx" :
        file = pd.read_excel(file)

    elif fileType == ".csv" :
        file = pd.read_csv(file)

    else : 
        file = "Not good type of file"
        return file

    file.rename(columns=str.lower, inplace=True)
    file = file.to_dict(orient='list')

    return file

def normalizePrices(parameters,file):
    
    file = getDataFromSheet(file)
    values = []

    for val in file[parameters[0]] :
        
        if isinstance(val,float) :
            values.append(val)
        
        elif isinstance(val,int) :
            val = str(val) + parameters[1]
            values.append(val)
        
        elif isinstance(val,str) :
            word = ""

            for letter in val :
                if isinstance(letter,int) :
                    word += str(letter)
                
                else :
                    word += parameters[1]
                    word += 'errata'
            
            values.append(word)
    
    print(values)
    return

def standardizeDates(parameters,file) :
    return

def standardizePhoneNumbers(parameters,file):
    return

def standardizeNames(parameters,file):
    return

def removeDuplicates(parameters,file) :

    return

def mergesFiles(parameters,file):
    return

def cleanColumns(file):
    #sert à uniformiser le nom des colonnes
    
    return file

def mergeFiles(parameters,file):
    return

normalizePrices(["prix","eu"],"./input/Try.xlsx")