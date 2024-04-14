## Functions to load data for embedding and analysis

# Libraries
import pandas as pd
import re


# Function to load txt data
def loadFile(fileName):
    
    with open(f'data/{fileName}.txt', 'r') as file:
        dictionary = "".join(file.read())

    return dictionary


# Function to load csv dataset in pandas dataframe
# Source: https://archive.ics.uci.edu/dataset/352/online+retail
def loadData(fileName):

    dataset = pd.read_csv(f'data/{fileName}.csv')
    dataset['InvoiceDate'] = pd.to_datetime(dataset['InvoiceDate'], format = '%m/%d/%Y')
    return dataset


# Function to improve llm generated chart code
def extract_code(response, chartNumber):

    # Extract code from markets
    startMarker = "```python"
    endMarker = "```"
    start = response.find(startMarker) + len(startMarker)
    end = response.find(endMarker, start)
    #codeSnippet = response[start:end].strip()
    #print(codeSnippet)

    if start != -1 and end != -1:

        code = response[start:end]
        
        # Change figsize parameters
        code = re.sub(r'plt\.figure\(figsize=\(\d+, \d+\)\)', 'plt.rcParams["figure.figsize"] = 8,3', code)

        # Add code to set background color, save chart pic
        adjustCode = f'''
plt.gcf().set_facecolor('#E1F2F5')\n    
plt.xticks(rotation = 0)\n
plt.savefig('./charts/chart{chartNumber}.jpg', format='jpg', bbox_inches = 'tight', dpi = 300)\n
plt.show()\n
'''
        
        # Split the string at plt.show()
        codeSplit = code.split("plt.show()")

        # Join parts with new text in between
        newCode = adjustCode.join(codeSplit)
        print(newCode)

        return newCode


# Modify prompt when chart is mentioned   
def promptChart(prompt):

    if 'chart' in prompt:
        prompt += 'Add python matplotlib.pyplot code for the chart.'
    else:
        prompt

    return prompt