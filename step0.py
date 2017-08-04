import numpy as np
import os
from openpyxl import Workbook

import pandas as pd


Sheet1 = "ModelList"
Sheet2 = "SheetWModelList"

fileNameStep0 = "step0.xlsx"
fileNameStep1 = "step1.xlsx"

columns = ["Module", "Path", "Scenario"]
columns2 = ["Module2", "Path2"]

writer = pd.ExcelWriter(fileNameStep0, engine='openpyxl')

dat = np.array([[0,0],[0,0]])
dat2 = np.array([[1,2],[3,4]])
df = pd.DataFrame(dat, columns=columns, index=None)
df2 = pd.DataFrame(dat2, columns=columns2, index=None)
df.to_excel(writer, Sheet1, index=False)
df2.to_excel(writer, "Tester", index=False)
writer.save()

# print("Fill in the excel spreadsheet opened, save it and close Excel")
# os.system("start " + fileNameStep0)

# while ('~$' + fileNameStep0 in os.listdir()):
#     pass

#Create first json script
pd.read_excel(fileNameStep0).to_json("modules.json")
df = pd.read_excel(fileNameStep0)
df = pd.read_json("mod1.2.json")
writer = pd.ExcelWriter("mod1.xlsx", engine='openpyxl')
df.to_excel(writer, "mod1", index=False)
writer.save()

print(df)