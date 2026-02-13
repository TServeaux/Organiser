import pandas as pd
import numpy as np
import os

numbers = ['0','1','2','3','4','5','6','7','8','9']
month = ['Junuary','February','March','April','Mai',
        'June','July','August','September','October',
        'November','December']

def getDataFromSheet(file):

    """
    This function transform the excel file into a matrix of data.
    Entry :
        - File (excel or csv)
    Output :
        - Matrix of data (dictionnary of list)
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

def normalizePrices(devise,columnName,file):
    
    """
    This function normalize prices.
    Entry :
        - File : dictionnary
        - ColumnName : Name of the column we want to change
        - Devise : devise of money
    Output :
        - Values : list of normalized prices
    """
    
    values = []

    for val in file[columnName] :
        
        if isinstance(val,float) :
            values.append(val)
        
        elif isinstance(val,int) :
            if val == 0 :
                values.append(np.nan)
                
            else :
                val = str(val) + devise
                values.append(val)
        
        elif isinstance(val,str) :
            word = ""

            for letter in val :
                if letter in numbers :
                    word += letter
                
                else :
                    word += devise
                    
            values.append(word)
    
    return values

def standardizeDates(parameters,file) :
    
    return

def standardizePhoneNumbers(columnName,parameters,file):
    return

def standardizeNames(columnName,captialize,file):
    """
    This function standardize names.
    Entry :
        - File : dictionnary
        - ColumnName : Name of the column we want to change
        - Captialize : boolean to know if you wnat the name full 
        capitalize or only the first letter
    Output :
        - Values : list of standardized names
    """
   
    names = []
    
    for val in file[columnName] :
        
        if isinstance(val,str) :
            
            val = val.split()
            standadizedName = []
            
            for name in val :
                word = ''
                
                firstLetter = True
                
                for letter in name :
                    if firstLetter :
                        word += letter.capitalize()
                        if not captialize :
                            firstLetter = False
                        
                    else :
                        word += letter.lower()
                        
                standadizedName.append(word)
            
            names.append(' '.join(standadizedName))
        
        else :
            names.append(val)
        
    return names

def removeDuplicates(file) :
    
    return file

def mergesFiles(parameters,file):
    return

def cleanColumns(file):
    #sert à uniformiser le nom des colonnes
    
    return file

def deleteRow(parameters,file):
    #la fct sert à supprimer des colonnes sur un critere (ex : pas d adresse mail, pas de nom ... etc)
    return

removeDuplicates("./input/Try.xlsx")