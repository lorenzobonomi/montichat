## Functions to load data for embedding and analysis

# Libraries
import pandas as pd


# Function to load txt data
def loadFile(fileName):
    
    with open(f'data/{fileName}.txt', 'r') as file:
        dictionary = "".join(file.read())

    return dictionary

# Function to load csv dataset in pandas dataframe
# https://archive.ics.uci.edu/dataset/352/online+retail
def loadData(fileName):
    dataset = pd.read_csv(f'data/{fileName}.csv')
    return dataset