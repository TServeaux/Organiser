import pandas as pd
import numpy as np
import os

def getDataFromSheet(file):
    """
    This function transform the excel file into a matrix of data.
    Entry :
        - File (excel or csv)
    Output :
        - Matrix of data
    """
    
    fileType = os.path.splitext(file)[1] # determine the type of the file
    
    if fileType == ".xlsx" :
        file = pd.read_excel(file)
    elif fileType == ".csv" :
        file = pd.read_csv(file)
    else : 
        file = "Pas bon type de fichier"
    
    return file

def normalizePrices(parameters,file):
    
    file = getDataFromSheet(file)
    print(file)
    
    for i,val in 
    
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

def cleanColumns(parameters,file):
    #sert à uniformiser le nom des colonnes
    
    return

def mergeFiles(parameters,file):
    return

normalizePrices("euro","./input/Try.xlsx")