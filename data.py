## Functions to load data for embedding and analysis

# Libraries
import pandas as pd
import re
import textwrap


# Function to load txt data
def loadFile(fileName):
    
    with open(f'data/{fileName}.txt', 'r') as file:
        dictionary = "".join(file.read())

    return dictionary

# Function to load csv dataset in pandas dataframe
# https://archive.ics.uci.edu/dataset/352/online+retail
def loadData(fileName):
    dataset = pd.read_csv(f'data/{fileName}.csv')
    dataset['InvoiceDate'] = pd.to_datetime(dataset['InvoiceDate'], format = '%m/%d/%Y')
    return dataset


def extract_code(response, chartNumber):

    start_marker = "```python"
    end_marker = "```"

# Extract code between markers
    start = response.find(start_marker) + len(start_marker)
    end = response.find(end_marker, start)
    code_snippet = response[start:end].strip()

    print(code_snippet)

    if start != -1 and end != -1:

        code = response[start:end]
        code = re.sub(r'plt\.figure\(figsize=\(\d+, \d+\)\)', 'plt.rcParams["figure.figsize"] = 8,3', code)
        # New text to insert
        adjustCode = f'''
plt.gcf().set_facecolor('#E1F2F5')\n    
plt.rcParams['font.serif'] = 'Times New Roman'\n
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
    #else:
        #return "No code found between '''"
    

def promptChart(prompt):

    if 'chart' in prompt:
        prompt += 'Add python matplotlib.pyplot code for the chart.'
    else:
        prompt

    return prompt