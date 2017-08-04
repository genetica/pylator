import pandas as pd
import os
import time

simFolder = ""

Sheet1 = "ModelList"
Sheet2 = "Matrix"
Sheet3 = "Globals"

sheet1Column1 = "Module"
sheet1Column2 = "Path"
sheet1Column3 = "Scenario"
sheet1Columns = [sheet1Column1, sheet1Column2, sheet1Column3]

simGlobals = {
"simulation" : {    "execution"     : { "step"          : 0,
                                        "time"          : 1},
                    "information"   : { "scenario"      : "default",
                                        "dateCreated"   : time.strftime("%d/%m/%Y")}
                },
"user"      :   { "image"           : { "height"        : 84,
                                        "width"         : 150}
            }
}



scenarioName = "default1"
fileName = "sim_" + scenarioName

excelFileNameModelList = simFolder + fileName + "_" + Sheet1 + ".xlsx"
excelFileNameMatrix    = simFolder + fileName + "_" + Sheet2 + ".xlsx"
excelFileNameGlobals   = simFolder + fileName + "_" + Sheet3 + ".xlsx"
excelFileName = simFolder + fileName + ".xlsx"

column1 = "Category"
column2 = "Property"
column3 = "Name"
columns = [column1, column2, column3]

sheet3Columns = [column1, column2, column3, "default"]

notModuleSheets = [Sheet1, Sheet2, Sheet3]

def isExcelFileOpen(file2Check, error = True):
    if ('~$' + file2Check in os.listdir()):
        print("ERROR: Close excel file", file2Check)
        if error:
            raise PermissionError    
        else:
            return True
    else:
        return False

def isExcelExisting(file2Check, error = True):
    if (file2Check in os.listdir()):
        return True 
    else:
        if error:
            print("ERROR: File not found,",file2Check)
            raise FileNotFoundError
        else:
            return False

def updateModelListFileFromSim():
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    isExcelFileOpen(excelFileNameMatrix)

    # Read main simulation file
    xl = pd.ExcelFile(excelFileName)

    # Update Model List 
    if (Sheet1 in xl.sheet_names):
        dfS = xl.parse(Sheet1)
        dfS.to_excel(excelFileNameModelList, Sheet1, index=False)
        #print("INFO: Updated,", excelFileNameModelList)
    else:
        print("ERROR: {} not found in {}".format(Sheet1,excelFileName))
        raise FileNotFoundError

    print("INFO: ModelList {} updated from {}".format(excelFileNameModelList, excelFileName))


def updateMatrixFilefromSim():
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    isExcelFileOpen(excelFileNameMatrix)

    # Read main simulation file
    xl = pd.ExcelFile(excelFileName)

    # Update Matrix file
    if (Sheet2 in xl.sheet_names):
        dfS = xl.parse(Sheet2,index_col=[0,1,2,3,4], header=[0,1,2,3,4])
        dfS.to_excel(excelFileNameMatrix, Sheet2)
        #print("INFO: Updated,", excelFileNameMatrix)
    else:
        print("ERROR: {} not found in {}".format(Sheet2,excelFileName))
        raise FileNotFoundError
  
    print("INFO: Matrix {} updated from {}".format(excelFileNameMatrix, excelFileName))


def updateGlobalsFileFromSim():
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    isExcelFileOpen(excelFileNameGlobals)

    # Read main simulation file
    xl = pd.ExcelFile(excelFileName)
   
    # Update Global variables.
    if (Sheet3 in xl.sheet_names):
        dfS = xl.parse(Sheet3, index_col =[0,1,2])
        dfS.to_excel(excelFileNameGlobals, Sheet3)
        #print("INFO: Updated,", excelFileNameGlobals)
    else:
        print("ERROR: {} not found in {}".format(Sheet3,excelFileName))
        raise FileNotFoundError

    print("INFO: Globals {} updated from {}".format(excelFileNameGlobals, excelFileName))



def updateFilesFromSim():
    """
        Function to store current simulation configuration (Not connected to the modules) to seperate files.
    """
    # Check if main simluation file exist
    isExcelExisting(excelFileName)

    # Check if files are open
    #isExcelFileOpen(excelFileName) # Not require to be closed.
    isExcelFileOpen(excelFileNameModelList)
    isExcelFileOpen(excelFileNameMatrix)
    isExcelFileOpen(excelFileNameGlobals)

    # Read main simulation file
    xl = pd.ExcelFile(excelFileName)

    # Update Model List 
    updateModelListFileFromSim()

    # Update Matrix file
    updateMatrixFilefromSim()
    
    # Update Global variables.
    updateGlobalsFileFromSim()

def updateSimFromModelListFile():
    # Check if main simulation file is open
    isExcelFileOpen(excelFileName)
    # other files are not required to be closed.

    # Check if required files exist
    isExcelExisting(excelFileName)
    isExcelExisting(excelFileNameModelList)

    xl = pd.ExcelFile(excelFileName)

    # Read Model List
    if not (Sheet1 in xl.sheet_names):
        df1 = pd.DataFrame([], columns=sheet1Columns)
    else:
        df1 = pd.read_excel(excelFileNameModelList)

    # Write excel file    
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    df1.to_excel(writer, Sheet1, index=False)
    
    for sheet in xl.sheet_names:
        if sheet == Sheet2:
            df2 = xl.parse(Sheet2,  index_col=[0,1,2,3,4], header=[0,1,2,3,4]) 
            df2.to_excel(writer, Sheet2)    

        elif ((sheet != Sheet1) and (sheet != Sheet2)):
            dfS = xl.parse(sheet, index_col =[0,1,2])
            dfS.to_excel(writer, sheet)

    writer.save()

    print("INFO: Sim {} updated from {}".format(excelFileName, excelFileNameModelList))

def updateSimFromMatrixFile():

    # Check if main simulation file is open
    isExcelFileOpen(excelFileName)
    # other files are not required to be closed.

    # Check if required files exist
    isExcelExisting(excelFileName)
    isExcelExisting(excelFileNameMatrix)

    xl = pd.ExcelFile(excelFileName)

    # Read curret matrix
    if not (Sheet2 in xl.sheet_names):
        df2 = pd.DataFrame([], columns=[])
    else:
        df2 = pd.read_excel(excelFileNameMatrix, sheetname=Sheet2,index_col=[0,1,2,3,4], header=[0,1,2,3,4])

    

    # Write excel file    
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    
    df1 = xl.parse(Sheet1)
    df1.to_excel(writer, Sheet1, index=False)   
    
    df2.to_excel(writer, Sheet2)    
   
    for sheet in xl.sheet_names:
        if ((sheet != Sheet1) and (sheet != Sheet2) ):
            dfS = xl.parse(sheet, index_col =[0,1,2])
            dfS.to_excel(writer, sheet)

    writer.save()       
    print("INFO: Sim {} updated from {}".format(excelFileName, excelFileNameMatrix))

def updateSimFromGlobalsFile():
    # Check if main simulation file is open
    isExcelFileOpen(excelFileName)
    # other files are not required to be closed.

    # Check if required files exist
    isExcelExisting(excelFileName)
    isExcelExisting(excelFileNameGlobals)

    xl = pd.ExcelFile(excelFileName)

    # Read globals
    if not (Sheet3 in xl.sheet_names):
        globalSheet = []
        for cat in simGlobals:
            for prop in simGlobals[cat]:
                for name in simGlobals[cat][prop]:
                    row = [cat, prop, name, simGlobals[cat][prop][name]]
                    globalSheet.append(row)

        df3 = pd.DataFrame(globalSheet, columns=sheet3Columns)
        df3.set_index(columns, inplace=True)
    else:
        df3 = pd.read_excel(excelFileNameGlobals, index_col =[0,1,2])
    

    # Write excel file    
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')

    df1 = xl.parse(Sheet1)
    df1.to_excel(writer, Sheet1, index=False)   
    
    df2 = xl.parse(Sheet2,index_col=[0,1,2,3,4], header=[0,1,2,3,4])
    df2.to_excel(writer, Sheet2)    
    
    df3.to_excel(writer, Sheet3)
   
    for sheet in xl.sheet_names:
        if ((sheet != Sheet1) and (sheet != Sheet2) and (sheet != Sheet3)):
            dfS = xl.parse(sheet, index_col =[0,1,2])
            dfS.to_excel(writer, sheet)

    writer.save() 

    print("INFO: Sim {} updated from {}".format(excelFileName, excelFileNameGlobals))

def updateSimFromFiles():
    """
        Function update simulation file from seperate configuration files (Not connected to the modules).
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

def createEmptySim(override = False):
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

def _createModelList():
    # Create empty Module List excel file
    isExcelFileOpen(excelFileName)


    df = pd.DataFrame([], columns=sheet1Columns)
    df.to_excel(excelFileName, index=False, sheet_name= Sheet1)

    print("Fill in the excel spreadsheet, save it and close Excel")
    os.system("start " + excelFileName)

    # Wait for excel to get populated and closed
    while ('~$' + excelFileName in os.listdir()):
        pass

    print("Available module selection completed.")

    return 0


def _getInputModules():
    # Create empty Module List excel file
    isExcelFileOpen(excelFileName)
    #isExcelExisting(excelFileName)

    try:
        df = pd.read_excel(excelFileName, sheetname=Sheet1)
        df.to_excel(excelFileName, index=False, sheet_name= Sheet1)
    except PermissionError:
        print("ERROR: Close excel file", excelFileName)
        raise PermissionError
    except FileNotFoundError:
        print("File created ", excelFileName)
        df = pd.DataFrame([], columns=sheet1Columns)
        df.to_excel(excelFileName, index=False, sheet_name= Sheet1)

    print("Fill in the excel spreadsheet, save it and close Excel")
    os.system("start " + excelFileName)

    # Wait for excel to get populated and closed
    while ('~$' + excelFileName in os.listdir()):
        pass

    print("Available module selection completed.")

    return 0

def getModulesForSim():
    isExcelFileOpen(excelFileName)
    isExcelExisting(excelFileName)

    xl = pd.ExcelFile(excelFileName)

    for sheet in notModuleSheets:
        if sheet not in xl.sheet_names:
            print("ERROR: Incomplete simulation file, missing ", sheet)
            raise ValueError
    
    # Get module list sheet from excel
    df = []
    df1 = xl.parse(Sheet1)
    df2 = xl.parse(Sheet2, index_col=[0,1,2,3,4], header=[0,1,2,3,4])
    df3 = xl.parse(Sheet3, index_col =[0,1,2])

    # Create List of all sheets and do not override already included modules
    modLst = xl.sheet_names[:]
    for sheet in notModuleSheets:
        modLst.remove(sheet)
    dfNames = []

    for idx in df1.index:
        if df1["Module"][idx] not in modLst:
            dfS = pd.read_excel(df1["Scenario"][idx], index_col =[0,1,2])
            df.append(dfS)
            dfNames.append(df1["Module"][idx])
            print("INFO: {} from {} inserted into {}".format(df1["Module"][idx], df1["Scenario"][idx],excelFileName))
        else:
            # Read current sheet
            dfS = xl.parse(df1["Module"][idx], index_col =[0,1,2])
            df.append(dfS)
            modLst.remove(df1["Module"][idx])
            dfNames.append(df1["Module"][idx])
            

    
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    df1.to_excel(writer, Sheet1, index=False)
    df2.to_excel(writer, Sheet2)
    df3.to_excel(writer, Sheet3)
    for idx, dfS in enumerate(df):
        dfS.to_excel(writer, dfNames[idx])
    writer.save()

    print("INFO: Modules updated in",excelFileName)


def updateSimFromScenarioFiles():
    isExcelFileOpen(excelFileName)
    isExcelExisting(excelFileName)

    xl = pd.ExcelFile(excelFileName)

    for sheet in notModuleSheets:
        if sheet not in xl.sheet_names:
            print("ERROR: Incomplete simulation file, missing ", sheet)
            raise ValueError
    
    # Get module list sheet from excel
    df = []
    df1 = xl.parse(Sheet1)
    df2 = xl.parse(Sheet2, index_col=[0,1,2,3,4], header=[0,1,2,3,4])
    df3 = xl.parse(Sheet3, index_col =[0,1,2])

    # Create List of all sheets and do not override already included modules
    modLst = xl.sheet_names[:]
    for sheet in notModuleSheets:
        modLst.remove(sheet)
    dfNames = []

    for idx in df1.index:
        # Read current sheet
        dfS = xl.parse(df1["Module"][idx], index_col =[0,1,2])
        df.append(dfS)
        modLst.remove(df1["Module"][idx])
        dfNames.append(df1["Module"][idx])
        print("INFO: {} from {} updated in {}".format(df1["Module"][idx], df1["Scenario"][idx],excelFileName))
    
    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    df1.to_excel(writer, Sheet1, index=False)
    df2.to_excel(writer, Sheet2)
    df3.to_excel(writer, Sheet3)
    for idx, dfS in enumerate(df):
        dfS.to_excel(writer, dfNames[idx])
    writer.save()

    print("INFO: Modules updated in",excelFileName)

def updateScenarioFilesFromSim():
    
    isExcelExisting(excelFileName)

    xl = pd.ExcelFile(excelFileName)

    for sheet in notModuleSheets:
        if sheet not in xl.sheet_names:
            print("ERROR: Incomplete simulation file, missing ", sheet)
            raise ValueError
    
    # Get module list sheet from excel
    df = []
    df1 = xl.parse(Sheet1)
    df2 = xl.parse(Sheet2, index_col=[0,1,2,3,4], header=[0,1,2,3,4])
    df3 = xl.parse(Sheet3, index_col =[0,1,2])

    # Create List of all sheets and do not override already included modules
    modLst = xl.sheet_names[:]
    for sheet in notModuleSheets:
        modLst.remove(sheet)
    dfNames = []

    for idx in df1.index:
        if df1["Module"][idx] not in modLst:
            print("WARNING: Module not loaded", df1["Module"][idx])
            
            df.append(dfS)
            dfNames.append(df1["Module"][idx])
        else:
            # Read current sheet
            dfS = xl.parse(df1["Module"][idx], index_col =[0,1,2])
            if not isExcelFileOpen(df1["Scenario"][idx]):
                dfS.to_excel(df1["Scenario"][idx], sheet_name=df1["Module"][idx])
                modLst.remove(df1["Module"][idx])
                print("INFO: {} at {} updated from {}".format(df1["Module"][idx], df1["Scenario"][idx],excelFileName))

    print("INFO: Done. Modules updated from", excelFileName)
    

def readSimIputs():
    #TODO
    inputDictionary = {}
    return inputDictionary

def createConnectivityMatrix():
    xl = pd.ExcelFile(excelFileName)

    if Sheet1 not in xl.sheet_names:
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
    for name in xl.sheet_names:
        if name not in notModuleSheets:
            dfNames.append(name)
            dfS = xl.parse(name, index_col =[0,1,2])
            df.append(dfS)
            dfS.drop(dfS.columns[[1,len(dfS.columns)-1]], axis=1, inplace = True)
            dfS = dfS[dfS.Exposed == True]

            dfSIn = dfS.loc["inputs"].copy()
            dfSIn.reset_index(inplace=True)
            dfSIn.drop("Exposed", axis=1, inplace=True)
            dfSIn.insert(0, "Module", [name]*len(dfSIn))
            dfSIn.insert(len(dfSIn.columns), "Index", [0]*len(dfSIn))
            for i in range(len(dfSIn)):
                dfSIn.set_value(i, "Index", inCnt)
                inCnt += 1
            if isinstance(dfIn, pd.DataFrame):
                dfIn = dfIn.append(dfSIn)
            else:
                dfIn = dfSIn.copy()

            dfSOut = dfS.loc["outputs"]
            dfSOut.reset_index(inplace=True)
            dfSOut.drop("Exposed", axis=1, inplace=True)
            dfSOut.insert(0, "Module", [name]*len(dfSOut))
            dfSOut.insert(len(dfSOut.columns), "Index", [0]*len(dfSOut))
            for i in range(len(dfSOut)):
                dfSOut.set_value(i, "Index", outCnt)
                outCnt += 1            
            if isinstance(dfOut, pd.DataFrame):
                dfOut = dfOut.append(dfSOut)
            else:
                dfOut = dfSOut.copy()            
            dfOut.append(dfSOut)
            
    dfIn.insert(0, "IO", ["Input"]*len(dfIn))
    dfIn.set_index(["IO","Module","Property", "Name","Index"], inplace=True)
    dfOut.insert(0, "IO", ["Output"]*len(dfOut))
    dfOut.set_index(["IO","Module", "Property", "Name","Index" ], inplace=True)
    

    col = dfOut.transpose().columns
    row = dfIn.index
    new = pd.DataFrame(index=row, columns=col)


    df = []
    dfNames = []
    for name in xl.sheet_names:
        if name == Sheet2:
            pass
        if name == Sheet1:
            dfNames.append(name)
            dfS = xl.parse(name)
            df.append(dfS)            
        else:
            dfNames.append(name)
            dfS = xl.parse(name, index_col =[0,1,2])
            df.append(dfS)

    df.insert(1, new)
    dfNames.insert(1, Sheet2)

    writer = pd.ExcelWriter(excelFileName, engine='openpyxl')
    for idx, dfS in enumerate(df):
        if idx == 0:
            dfS.to_excel(writer, dfNames[idx], index=False)
        else:
            dfS.to_excel(writer, dfNames[idx])
    writer.save()

    print("Assign crosses in the appropriate block")
    os.system("start " + excelFileName)

    # Wait for excel to get populated and closed
    while ('~$' + excelFileName in os.listdir()):
        pass

    print("Matrix Configuration completed.")
    return 0 

def readConnectivityMatrix():
    xl = pd.ExcelFile(excelFileName)

    if Sheet1 not in xl.sheet_names:
        print("ERROR: Incorrect excelfile")
        raise Exception
    if '~$' + excelFileName in os.listdir():
        print("ERROR: Close excel file", excelFileName)
        raise PermissionError

    tdf = pd.read_excel(excelFileName, sheetname=Sheet2,index_col=[0,1,2,3,4], header=[0,1,2,3,4])

    #xl.parse(name, index_col =[0,1,2])

    print(tdf)
    print(tdf.values)
    print(tdf.index[0])
    print(tdf.columns[0])
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

if __name__ == "__main__":
    #try:
    #getInputModules()
    #    pass
    #except PermissionError:
    #    pass
    #getScenarioFiles()
    
    #readConnectivityMatrix()
    #createEmptySim(True)
    #updateScenarioFiles()
    #updateSimFromFiles()
    #updateFilesFromSim()
    #updateSimToFiles()
    #updateSimFromScenarioFiles()
    getModulesForSim()
    #createConnectivityMatrix()
    #updateScenarioFilesFromSim()