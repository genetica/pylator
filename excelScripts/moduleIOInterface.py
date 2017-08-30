import numpy as np
import os
import pandas as pd

# Create Modules Base Interface spreadsheet

fileName = "module"
excelFileName = fileName + ".xlsx"
jsonFileName = fileName + ".json"

column1 = "Category"
column2 = "Property"
column3 = "Name"

base = 3
columns = [column1, column2, column3, "Exposed", "Description", "default", "type", "dimensions",  "size"]

initialData = {
"constants" : { "model1"  : ["pi", "exp"],
                "model2"  : ["threshold"],
                "model3"  : ["threshold"]
            },
"inputs"    : { "control"  : ["active"],
                "settings" : ["speed", "updateRate"],
                "data"     : ["pipeline"]
            },
"outputs"   : { "control"  : ["calibrate"],
                "settings" : [""],
                "data"     : ["pipeline"]
            }
}

data = []
for cat in initialData:
    for prop in initialData[cat]:
        for name in initialData[cat][prop]:
            row = [cat, prop, name, True]
            for idx in range(len(columns) - base - 1):
                row.append(None)
            data.append(row)

df = pd.DataFrame(data= data, columns= columns)
#df.to_json(jsonFileName)
df.set_index([column1, column2, column3], inplace=True)
df.to_excel(excelFileName)
print(df)


# #a = pd.read_json("ttt.json")
# #print(a)
# a = pd.read_excel("step0.xlsx", index_col=[0,1,2])
# #a = pd.read_excel("step0.xlsx")

# print(a)
# a.to_json("ttt.json")

# a.reset_index(inplace=True) 
# print(a)
# a.set_index(['Category', 'Property', 'Name'], inplace=True)
# a.to_excel("ttt.xlsx")
# #a = pd.read_json("ttt.json")
# print(a)
# #print(a.index)
# #print(a[['Input']].columns)