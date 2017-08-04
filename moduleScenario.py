import numpy as np
import os
import shutil
import pandas as pd

# Create module scenario file

scenarioName = "default"

fileName = "module"
excelFileName = fileName + ".xlsx"
excelScenario = fileName + "_" + scenarioName +".xlsx"


shutil.copy("./" + excelFileName, "./" + excelScenario)
#df = pd.read_excel(excelFileName, index_col=[0,1,2])



