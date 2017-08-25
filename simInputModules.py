"""
    simInputModules
"""

import pandas as pd
import numpy as np
import multiprocessing as mp
import os
import time

# default globals inputs
simGlobals = {
    "simulation" : {"execution"     : {"step"          : 0,
                                       "time"          : 1},
                    "information"   : {"scenario"      : "default",
                                       "dateCreated"   : time.strftime("%d/%m/%Y")}
                   },
    "user"       : {"image"         : {"height"        : 84,
                                       "width"         : 150}
                   }
}

Sheet1 = "ModelList"
Sheet2 = "Matrix"
Sheet3 = "Globals"

sheet1Column1 = "Module"
sheet1Column2 = "Path"
sheet1Column3 = "Scenario"
sheet1Columns = [sheet1Column1, sheet1Column2, sheet1Column3]

column1 = "Category"
column2 = "Property"
column3 = "Name"
columns = [column1, column2, column3]

sheet3Columns = [column1, column2, column3, "default"]

notModuleSheets = [Sheet1, Sheet2, Sheet3]


simFolder = ""

scenarioName = "default1"

fileName = "sim_" + scenarioName
excelFileNameModelList = simFolder + fileName + "_" + Sheet1 + ".xlsx"
excelFileNameMatrix = simFolder + fileName + "_" + Sheet2 + ".xlsx"
excelFileNameGlobals = simFolder + fileName + "_" + Sheet3 + ".xlsx"
excelFileName = simFolder + fileName + ".xlsx"

def isExcelFileOpen(file2Check, error=True):
    """
        isExcelFileOpen
    """
    if '~$' + file2Check in os.listdir():
        print("ERROR: Close excel file", file2Check)
        if error:
            raise PermissionError
        else:
            return True
    else:
        return False

def isExcelExisting(file2Check, error=True):
    """
        isExcelExisting
    """
    if file2Check in os.listdir():
        return True
    else:
        if error:
            print("ERROR: File not found,", file2Check)
            raise FileNotFoundError
        else:
            return False

def updateModelListFileFromSim():
    """
        updateModelListFileFromSim
    """
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    isExcelFileOpen(excelFileNameMatrix)

    # Read main simulation file
    dfxl = pd.ExcelFile(excelFileName)

    # Update Model List
    if Sheet1 in dfxl.sheet_names:
        dfs = dfxl.parse(Sheet1)
        dfs.to_excel(excelFileNameModelList, Sheet1, index=False)
        #print("INFO: Updated,", excelFileNameModelList)
    else:
        print("ERROR: {} not found in {}".format(Sheet1, excelFileName))
        raise FileNotFoundError

    print("INFO: ModelList {} updated from {}".format(excelFileNameModelList, excelFileName))


def updateMatrixFilefromSim():
    """
        updateMatrixFilefromSim
    """
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    isExcelFileOpen(excelFileNameMatrix)

    # Read main simulation file
    dfxl = pd.ExcelFile(excelFileName)

    # Update Matrix file
    if Sheet2 in dfxl.sheet_names:
        dfs = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])
        dfs.to_excel(excelFileNameMatrix, Sheet2)
        #print("INFO: Updated,", excelFileNameMatrix)
    else:
        print("ERROR: {} not found in {}".format(Sheet2, excelFileName))
        raise FileNotFoundError

    print("INFO: Matrix {} updated from {}".format(excelFileNameMatrix, excelFileName))


def updateGlobalsFileFromSim():
    """
        updateGlobalsFileFromSim
    """
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    isExcelFileOpen(excelFileNameGlobals)

    # Read main simulation file
    dfxl = pd.ExcelFile(excelFileName)

    # Update Global variables.
    if Sheet3 in dfxl.sheet_names:
        dfs = dfxl.parse(Sheet3, index_col=[0, 1, 2])
        dfs.to_excel(excelFileNameGlobals, Sheet3)
        #print("INFO: Updated,", excelFileNameGlobals)
    else:
        print("ERROR: {} not found in {}".format(Sheet3, excelFileName))
        raise FileNotFoundError

    print("INFO: Globals {} updated from {}".format(excelFileNameGlobals, excelFileName))


def updateFilesFromSim():
    """
        Function to store current simulation configuration (Not connected to the modules)
        to seperate files.
    """
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    #isExcelFileOpen(excelFileName) # Not require to be closed.
    isExcelFileOpen(excelFileNameModelList)
    isExcelFileOpen(excelFileNameMatrix)
    isExcelFileOpen(excelFileNameGlobals)

    # Read main simulation file
    #dfxl = pd.ExcelFile(excelFileName)

    # Update Model List
    updateModelListFileFromSim()

    # Update Matrix file
    updateMatrixFilefromSim()

    # Update Global variables.
    updateGlobalsFileFromSim()


def updateSimFromModelListFile():
    """
        updateSimFromModelListFile
    """
    # Check if main simulation file is open
    isExcelFileOpen(excelFileName)
    # other files are not required to be closed.

    # Check if required files exist
    isExcelExisting(excelFileName)
    isExcelExisting(excelFileNameModelList)

    dfxl = pd.ExcelFile(excelFileName)

    # Read Model List
    df1 = None
    if not Sheet1 in dfxl.sheet_names:
        df1 = pd.DataFrame([], columns=sheet1Columns)
    else:
        df1 = pd.read_excel(excelFileNameModelList)

    # Write excel file
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    df1.to_excel(writer, Sheet1, index=False)

    for sheet in dfxl.sheet_names:
        if sheet == Sheet2:
            df2 = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])
            df2.to_excel(writer, Sheet2)
        elif (sheet != Sheet1) and (sheet != Sheet2):
            dfs = dfxl.parse(sheet, index_col=[0, 1, 2])
            dfs.to_excel(writer, sheet)

    writer.save()

    print("INFO: Sim {} updated from {}".format(excelFileName, excelFileNameModelList))


def updateSimFromMatrixFile():
    """
        updateSimFromMatrixFile
    """

    # Check if main simulation file is open
    isExcelFileOpen(excelFileName)
    # other files are not required to be closed.

    # Check if required files exist
    isExcelExisting(excelFileName)
    isExcelExisting(excelFileNameMatrix)

    dfxl = pd.ExcelFile(excelFileName)

    # Read curret matrix
    df2 = None
    if not Sheet2 in dfxl.sheet_names:
        df2 = pd.DataFrame([], columns=[])
    else:
        df2 = pd.read_excel(excelFileNameMatrix, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])

    # Write excel file
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')

    df1 = dfxl.parse(Sheet1)
    df1.to_excel(writer, Sheet1, index=False)
    df2.to_excel(writer, Sheet2)

    for sheet in dfxl.sheet_names:
        if (sheet != Sheet1) and (sheet != Sheet2):
            dfs = dfxl.parse(sheet, index_col=[0, 1, 2])
            dfs.to_excel(writer, sheet)

    writer.save()
    print("INFO: Sim {} updated from {}".format(excelFileName, excelFileNameMatrix))


def updateSimFromGlobalsFile():
    """
        updateSimFromGlobalsFile
    """
    # Check if main simulation file is open
    isExcelFileOpen(excelFileName)
    # other files are not required to be closed.

    # Check if required files exist
    isExcelExisting(excelFileName)
    isExcelExisting(excelFileNameGlobals)

    dfxl = pd.ExcelFile(excelFileName)

    # Read globals
    df3 = None
    if not Sheet3 in dfxl.sheet_names:
        globalSheet = []
        for cat in simGlobals:
            for prop in simGlobals[cat]:
                for name in simGlobals[cat][prop]:
                    row = [cat, prop, name, simGlobals[cat][prop][name]]
                    globalSheet.append(row)

        df3 = pd.DataFrame(globalSheet, columns=sheet3Columns)
        df3.set_index(columns, inplace=True)
    else:
        df3 = pd.read_excel(excelFileNameGlobals, index_col=[0, 1, 2])

    # Write excel file
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')

    df1 = dfxl.parse(Sheet1)
    df1.to_excel(writer, Sheet1, index=False)

    df2 = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])
    df2.to_excel(writer, Sheet2)

    df3.to_excel(writer, Sheet3)

    for sheet in dfxl.sheet_names:
        if (sheet != Sheet1) and (sheet != Sheet2) and (sheet != Sheet3):
            dfs = dfxl.parse(sheet, index_col=[0, 1, 2])
            dfs.to_excel(writer, sheet)

    writer.save()

    print("INFO: Sim {} updated from {}".format(excelFileName, excelFileNameGlobals))


def updateSimFromFiles():
    """
        Function update simulation file from seperate configuration files
        (Not connected to the modules).
    """
    # Check if main simulation file is open
    isExcelFileOpen(excelFileName)
    # other files are not required to be closed.

    # Check if required files exist
    isExcelExisting(excelFileName)
    isExcelExisting(excelFileNameModelList)
    isExcelExisting(excelFileNameMatrix)
    isExcelExisting(excelFileNameGlobals)

    updateSimFromModelListFile()
    updateSimFromMatrixFile()
    updateSimFromGlobalsFile()


def createEmptySim(override=False):
    """
        createEmptySim
    """
    isExcelFileOpen(excelFileName)

    if isExcelExisting(excelFileName):
        if override:
            print("INFO: Simulation scenario exist. Overriding file", excelFileName)
        else:
            print("ERROR: Simulation scenario exist.")
            raise PermissionError

    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    df1 = pd.DataFrame([], columns=sheet1Columns)
    df1.to_excel(writer, Sheet1, index=False)
    df2 = pd.DataFrame([], columns=[])
    df2.to_excel(writer, Sheet2)

    globalSheet = []
    for cat in simGlobals:
        for prop in simGlobals[cat]:
            for name in simGlobals[cat][prop]:
                row = [cat, prop, name, simGlobals[cat][prop][name]]
                globalSheet.append(row)

    df3 = pd.DataFrame(globalSheet, columns=sheet3Columns)
    df3.set_index(columns, inplace=True)
    df3.to_excel(writer, Sheet3)

    writer.save()

    print("INFO: Created", excelFileName)

    # print("Fill in the excel spreadsheet, save it and close Excel")
    # os.system("start " + excelFileName)

    # # Wait for excel to get populated and closed
    # while ('~$' + excelFileName in os.listdir()):
    #     pass

    # print("Available module selection completed.")

    return 0


def getModulesForSim():
    """
        getModulesForSim
    """
    isExcelFileOpen(excelFileName)
    isExcelExisting(excelFileName)

    dfxl = pd.ExcelFile(excelFileName)

    for sheet in notModuleSheets:
        if sheet not in dfxl.sheet_names:
            print("ERROR: Incomplete simulation file, missing ", sheet)
            raise ValueError

    # Get module list sheet from excel
    df = []
    df1 = dfxl.parse(Sheet1)
    df2 = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])
    df3 = dfxl.parse(Sheet3, index_col=[0, 1, 2])

    # Create List of all sheets and do not override already included modules
    modLst = dfxl.sheet_names[:]
    for sheet in notModuleSheets:
        modLst.remove(sheet)
    dfNames = []

    for idx in df1.index:
        if df1["Module"][idx] not in modLst:
            dfs = pd.read_excel(df1["Scenario"][idx], index_col=[0, 1, 2])
            df.append(dfs)
            dfNames.append(df1["Module"][idx])
            print("INFO: {} from {} inserted into \
                  {}".format(df1["Module"][idx], df1["Scenario"][idx], excelFileName))
        else:
            # Read current sheet
            dfs = dfxl.parse(df1["Module"][idx], index_col=[0, 1, 2])
            df.append(dfs)
            modLst.remove(df1["Module"][idx])
            dfNames.append(df1["Module"][idx])



    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    df1.to_excel(writer, Sheet1, index=False)
    df2.to_excel(writer, Sheet2)
    df3.to_excel(writer, Sheet3)
    for idx, dfs in enumerate(df):
        dfs.to_excel(writer, dfNames[idx])
    writer.save()

    print("INFO: Modules updated in", excelFileName)


def updateSimFromScenarioFiles():
    """
        updateSimFromScenarioFiles
    """
    isExcelFileOpen(excelFileName)
    isExcelExisting(excelFileName)

    dfxl = pd.ExcelFile(excelFileName)

    for sheet in notModuleSheets:
        if sheet not in dfxl.sheet_names:
            print("ERROR: Incomplete simulation file, missing ", sheet)
            raise ValueError

    # Get module list sheet from excel
    df = []
    df1 = dfxl.parse(Sheet1)
    df2 = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])
    df3 = dfxl.parse(Sheet3, index_col=[0, 1, 2])

    # Create List of all sheets and do not override already included modules
    modLst = dfxl.sheet_names[:]
    for sheet in notModuleSheets:
        modLst.remove(sheet)
    dfNames = []

    for idx in df1.index:
        # Read current sheet
        dfs = dfxl.parse(df1["Module"][idx], index_col=[0, 1, 2])
        df.append(dfs)
        modLst.remove(df1["Module"][idx])
        dfNames.append(df1["Module"][idx])
        print("INFO: {} from {} updated in \
               {}".format(df1["Module"][idx], df1["Scenario"][idx], excelFileName))

    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    df1.to_excel(writer, Sheet1, index=False)
    df2.to_excel(writer, Sheet2)
    df3.to_excel(writer, Sheet3)
    for idx, dfs in enumerate(df):
        dfs.to_excel(writer, dfNames[idx])
    writer.save()

    print("INFO: Modules updated in", excelFileName)


def updateScenarioFilesFromSim():
    """
        updateScenarioFilesFromSim
    """
    isExcelExisting(excelFileName)

    dfxl = pd.ExcelFile(excelFileName)

    for sheet in notModuleSheets:
        if sheet not in dfxl.sheet_names:
            print("ERROR: Incomplete simulation file, missing ", sheet)
            raise ValueError

    # Get module list sheet from excel
    #df = []
    df1 = dfxl.parse(Sheet1)
    #df2 = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])
    #df3 = dfxl.parse(Sheet3, index_col=[0, 1, 2])

    # Create List of all sheets and do not override already included modules
    for idx in df1.index:
        if df1["Module"][idx] not in dfxl.sheet_names[:]:
            print("WARNING: Module not loaded", df1["Module"][idx])
        else:
            # Read current sheet
            dfs = dfxl.parse(df1["Module"][idx], index_col=[0, 1, 2])
            if not isExcelFileOpen(df1["Scenario"][idx]):
                dfs.to_excel(df1["Scenario"][idx], sheet_name=df1["Module"][idx])
                print("INFO: {} at {} updated from \
                       {}".format(df1["Module"][idx], df1["Scenario"][idx], excelFileName))

    print("INFO: Done. Modules updated from", excelFileName)


def createConnectivityMatrix():
    """
        createConnectivityMatrix
    """
    dfxl = pd.ExcelFile(excelFileName)

    if Sheet1 not in dfxl.sheet_names:
        print("ERROR: Incorrect excelfile")
        raise Exception
    if '~$' + excelFileName in os.listdir():
        print("ERROR: Close excel file", excelFileName)
        raise PermissionError

    # Get module list sheet from excel
    df = []
    dfIn = None
    dfOut = []
    dfNames = []
    inCnt = 0
    outCnt = 0

    name = "Globals"
    dfNames.append(name)
    dfs = dfxl.parse(name, index_col=[0, 1, 2])
    df.append(dfs)

    dfsOut = dfs.copy()
    dfsOut.reset_index(inplace=True)
    dfsOut.insert(len(dfsOut.columns), "Index", [0]*len(dfsOut))
    for i in range(len(dfsOut)):
        dfsOut.set_value(i, "Index", outCnt)
        outCnt += 1
    dfOut = dfsOut.copy()

    for name in dfxl.sheet_names:
        if name not in notModuleSheets:
            dfNames.append(name)
            dfs = dfxl.parse(name, index_col=[0, 1, 2])
            df.append(dfs)
            dfs.drop(dfs.columns[[1, len(dfs.columns)-1]], axis=1, inplace=True)
            dfs = dfs[dfs.Exposed == True]

            dfsIn = dfs.loc["inputs"].copy()
            dfsIn.reset_index(inplace=True)
            dfsIn.drop("Exposed", axis=1, inplace=True)
            dfsIn.insert(0, "Module", [name]*len(dfsIn))
            dfsIn.insert(len(dfsIn.columns), "Index", [0]*len(dfsIn))
            for i in range(len(dfsIn)):
                dfsIn.set_value(i, "Index", inCnt)
                inCnt += 1
            if isinstance(dfIn, pd.DataFrame):
                dfIn = dfIn.append(dfsIn)
            else:
                dfIn = dfsIn.copy()

            dfsOut = dfs.loc["outputs"]
            dfsOut.reset_index(inplace=True)
            dfsOut.drop("Exposed", axis=1, inplace=True)
            dfsOut.insert(0, "Module", [name]*len(dfsOut))
            dfsOut.insert(len(dfsOut.columns), "Index", [0]*len(dfsOut))
            for i in range(len(dfsOut)):
                dfsOut.set_value(i, "Index", outCnt)
                outCnt += 1
            if isinstance(dfOut, pd.DataFrame):
                dfOut = dfOut.append(dfsOut)
            else:
                dfOut = dfsOut.copy()
            dfOut.append(dfsOut)

    dfIn.insert(0, "IO", ["Input"]*len(dfIn))
    dfIn.reset_index(inplace=True)
    dfIn.set_index(["IO", "Module", "Property", "Name", "Index"], inplace=True)

    dfOut.reset_index(inplace=True)
    dfOut.insert(0, "IO", ["Output" for a in range(len(dfOut))])
    if 'index' in dfOut.columns:
        dfOut.drop("index", axis=1, inplace=True)
    for i in range(len(df[0])):
        dfOut.set_value(i, "IO", "Globals")
        dfOut.set_value(i, "Module", dfOut["Category"][i])
    dfOut.drop("Category", axis=1, inplace=True)
    dfOut.set_index(["IO", "Module", "Property", "Name", "Index"], inplace=True)

    col = dfOut.transpose().columns
    row = dfIn.index
    new = pd.DataFrame(index=row, columns=col)

    df = []
    dfNames = []
    for name in dfxl.sheet_names:

        if name == Sheet2:
            pass
        elif name == Sheet1:
            dfNames.append(name)
            dfs = dfxl.parse(name)
            df.append(dfs)
        else:
            dfNames.append(name)
            dfs = dfxl.parse(name, index_col=[0, 1, 2])
            df.append(dfs)

    df.insert(1, new)
    dfNames.insert(1, Sheet2)

    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    for idx, dfs in enumerate(df):
        if idx == 0:
            dfs.to_excel(writer, dfNames[idx], index=False)
        else:
            dfs.to_excel(writer, dfNames[idx])
    writer.save()

    # print("Assign crosses in the appropriate block")
    # os.system("start " + excelFileName)

    # # Wait for excel to get populated and closed
    # while ('~$' + excelFileName in os.listdir()):
    #     pass

    # print("Matrix Configuration completed.")
    return 0


def __getModuleData__(simData, name, dfs):
    """
    Read the specified module scenario file provided as a pandas dataframe (dfs)
    and store it in the dictionary simData with reference to name.

    """
    pass


def getVariableValue(simData, variable):
    """
        getVariableValue
    """
    if isinstance(variable, str):
        if variable[0] == '/':
            if len(variable.split(" ")) == 1:
                if variable in simData:
                    return getVariableValue(simData, simData[variable])
                else:
                    print("ERROR:", variable, ":Not found.")
                    raise ValueError
            elif len(variable.split(" ")) > 1:
                result = ""
                for var in variable.split(" "):
                    if var in simData:
                        result += str(getVariableValue(simData, simData[var])) + " "
                    else:
                        print("ERROR:", variable, ":Not found.")
                        raise ValueError

                return result.strip()
            else:
                print("ERROR:", variable, ":Unkown state.")
                raise ValueError
        else:
            return variable
    else:
        return variable


def loadDataFromFile(filename):
    """
        loadDataFromFile
    """
    print("TODO: load initial values from file,folder,script etc.")
    raise ValueError
    return 0


def __calculateInitialValue__(simData, idx, dfs, name_prefix="/"):
    """
    All inputs/outputs must have initial values which can be either an array,
    integer, double, bool, string. All arrays are placed as numpy arrays of type int64,
    float64. Data size must be fixed at simulation time and can contain globals
    that do no change. Variables that change during simulation are inputs and
    are linked through the connectivity matrix.

    default type dimensions size

    default- value or link to script that will create a data object with data
             with the specified attributes. Or the default value of all elements
             in an array.
             Use "random [min] [max]" to populate an array with uniform distributed values.
    type - "int", "float", "str"
    dimensions - amount of dimensions in array
    size - size of dimensions

    Examples.
      Single scalar value.
    default type    dimensions  size
    12      int     0           1

      vector point at position 0 - >[0, 0, 0]
    default type    dimensions  size
    0       int     1           3
    """
    key = name_prefix + "/".join(dfs.index[idx])

    default = getVariableValue(simData, dfs.ix[idx]["default"])

    typeV = getVariableValue(simData, dfs.ix[idx]["type"])

    dimensions = getVariableValue(simData, dfs.ix[idx]["dimensions"])

    size = getVariableValue(simData, dfs.ix[idx]["size"])

    if dimensions > 0:
        if isinstance(size, str):
            size = size.strip().split(" ")
        else:
            size = [str(size)]
        shape = []
        for d in size:
            shape.append(int(d))
        shape = tuple(shape)
        array = np.ones(shape)
    else:
        array = np.ones((1))

    if isinstance(default, str) and typeV != "str":
        default = loadDataFromFile(default)
    elif typeV == "int":
        default = default * array
        default = np.array(default, np.int_)
    elif typeV == "float":
        default = default * array
        default = np.array(default, np.float_)
    elif typeV == "bool":
        default = default * array
        default = np.array(default, np.bool_)
    elif typeV == "str":
        pass
    else:
        print("ERROR: Unknown 'type' in module", name, "initial values.")
        raise ValueError

    if isinstance(default, str):
        simData[key] = default
    elif default.size == 1:
        simData[key] = default[0]
    else:
        simData[key] = default

    return 0

def readConnectivityMatrix():
    """
        readConnectivityMatrix
    """
    isExcelExisting(excelFileName)

    dfxl = pd.ExcelFile(excelFileName)
    if Sheet1 not in dfxl.sheet_names:
        print("ERROR: Incorrect excelfile")
        raise Exception

    connectivityMatrix = {}

    #dfS = pd.read_excel(excelFileName, sheetname=Sheet2,index_col=[0,1,2,3,4], header=[0,1,2,3,4])
    dfs = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2,3 ,4])


    #xl.parse(name, index_col =[0,1,2])

    #print(dfs)
    #print(dfs.values)
    #print(dfs.index[0])
    #print(dfs.columns[0])
    
    for idx, row in enumerate(dfs.index):


        cnt = 0
        inputKey = "/" + row[1] + "/input/" + row[2] + \
                   "/" + row[3]
        for col, val in enumerate(dfs.values[idx]):
            if not isinstance(val, float):
                outputKey = "/" + dfs.columns[col][1] + "/output/" + dfs.columns[col][2] + \
                         "/" + dfs.columns[col][3]
                connectivityMatrix[inputKey] = outputKey
                cnt += 1
                #print("{} {}".format(inputKey, outputKey))

        # Error checking
        if cnt > 1:
            print("ERROR: Variable", row, " has multiple inputs.")
            raise ValueError
        elif cnt == 0:
            print("ERROR: Variable", row, " has no inputs.")
            raise ValueError
            
    
    for key, value in connectivityMatrix.items():
        print("{} {}".format(key, value))

    # # Get module list sheet from excel
    # df = []
    # dfIn = None
    # dfOut = []
    # dfNames = []
    # inCnt = 0
    # outCnt = 0
    # for name in xl.sheet_names:
    #     if name ==  Sheet2:
    #         pass
    #     elif name != Sheet1:
    #         dfNames.append(name)
    #         dfS = xl.parse(name, index_col =[0,1,2])
    #         df.append(dfS)
    #         dfS.drop(dfS.columns[[1,len(dfS.columns)-1]], axis=1, inplace = True)
    #         dfS = dfS[dfS.Exposed == True]

    return connectivityMatrix

def getSimData():
    """
        getSimData
    """
    #isExcelFileOpen(excelFileName)
    isExcelExisting(excelFileName)

    dfxl = pd.ExcelFile(excelFileName)

    for sheet in notModuleSheets:
        if sheet not in dfxl.sheet_names:
            print("ERROR: Incomplete simulation file, missing ", sheet)
            raise ValueError

    # Get module list sheet from excel
    df = []
    df1 = dfxl.parse(Sheet1)
    df2 = dfxl.parse(Sheet2, index_col=[0, 1, 2, 3, 4], header=[0, 1, 2, 3, 4])
    df3 = dfxl.parse(Sheet3, index_col=[0, 1, 2])

    simData = {}
    simData["/modules/names"] = []
    simData["/modules/paths"] = []
    simData["/modules/scenario"] = []

    #Modlist
    for idx in df1.index:
        simData["/modules/names"].append(df1["Module"][idx])
        simData["/modules/paths"].append(df1["Path"][idx])
        simData["/modules/scenario"].append(df1["Scenario"][idx])

    for i in range(len(df3.index)):
        __calculateInitialValue__(simData, i, df3)

    # Create List of all sheets and do not override already included modules
    for idx in df1.index:
        if df1["Module"][idx] not in dfxl.sheet_names[:]:
            #dfs = pd.read_excel(df1["Scenario"][idx], index_col =[0,1,2])
            #df.append(dfs)
            #dfNames.append(df1["Module"][idx])
            print("ERROR: Incomplete simulation file, missing ", df1["Module"][idx])
            raise ValueError
        else:
            # Read current sheet
            dfs = dfxl.parse(df1["Module"][idx], index_col=[0, 1, 2])
            for i in range(len(dfs.index)):
                __calculateInitialValue__(simData, i, dfs)
            # Rename all module specific variables
            # this is to allow loca referencing and global referencing.
            # modules can not reference variables in other modules.
            # modules can not consist variables that is also present in the global list.
            for i in range(len(dfs.index)):
                key = "/" + "/".join(dfs.index[i])
                new_key = "/" + df1["Module"][idx] + key
                simData[new_key] = simData.pop(key)

    return simData


def printSimData(simData, showMatrix=False):
    """
        printSimData
    """
    for key, value in simData.items():
        if isinstance(value, np.ndarray):
            if showMatrix:
                print('{:41}'.format(key) + str(value).replace('\n', '\n{:41}'.format("")))
            else:
                print('{:40} {} {}'.format(key, value.dtype, value.shape))
        else:
            print("{:40} {}".format(key, value))



def convertSimData2CTypes(simData):
    """
        convertSimData2CTypes
    """


    return simData

if __name__ == "__main__":
    #try:
    #getInputModules()
    #    pass
    #except PermissionError:
    #    pass
    #getScenarioFiles()

    #readConnectivityMatrix()
    #createEmptySim(True)

    #updateSimFromFiles()
    #updateFilesFromSim()
    #updateSimFromScenarioFiles()
    #updateSimFromMatrixFile()
    #updateMatrixFilefromSim()
    #getModulesForSim()
    #createConnectivityMatrix()
    #updateScenarioFilesFromSim()
    #createConnectivityMatrix()
    simData = getSimData()
    simData = convertSimData2CTypes(simData)
    printSimData(simData)

    readConnectivityMatrix()
