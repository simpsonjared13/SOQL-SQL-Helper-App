#odsscript 
from OdsHelper import *

def salesforceToOracleScripter(path,folder,scriptName,dictionaryName,schema,tableName,tableSpace,storage): """ Declare Variables """ # path = input("Enter the file path of the file to read: ") # fileToRead = input("Enter the file name without .txt: ")

# file = open(path+fileToRead+".txt", "r")
file = open(path, "r")


# scriptName = input("Enter a name without .txt for the new script file: ")
# newFile = open(path+scriptName+".txt", "w")
newFile = open(folder+'/'+scriptName+".txt", "w")
newDataDict = open(folder+'/'+dictionaryName+".txt", "w")
f=""
forms = open(folder+"/" + scriptName + " formulas.txt", "w")
d = dict()
uniqueTypes = dict()
#salesForceTypes is a dictionary acquired from the OdsHelper Class
salesForceTypes = getSalesForceTypes()
"""
End of variable declarations
"""

"""
Begin string manuipulation to format it for creating a query.
"""
for x in file:
    arr = x.split(",")
    fieldName = arr[0].split(":")[1][:]
    dataType = arr[1].split(":")[1][:]
    stringLength = arr[2].split(":")[1][:]
    precision = arr[3].split(":")[1][:]
    isNull = arr[4].split(":")[1][:]
    scale = arr[5].split(":")[1][:]
    label = arr[9].split(":")[1][:]
    formula = arr[10].split(":")[1][:-1]
    #comment out next if depending on if you use formulas in an ODS
    if formula == "false":
        if fieldName == "Id":
            isNull = "NOT NULL"
        if dataType == "DOUBLE" or dataType =="PERCENT" or dataType == "CURRENCY":
            d.update({fieldName: [dataType,precision,scale,isNull,label]}) 
        else:
            d.update({fieldName: [dataType,stringLength,isNull,label]}) 
        u = uniqueTypes.get(dataType)
        if u != None:
            uniqueTypes.update({dataType: u+1})
        else:
            uniqueTypes.update({dataType: 1})
    else:
        f+= fieldName + "\n"
"""
End of query prepper
"""
# schema = input("Eneter the Schema Name: ")
# tableName = input("Enter the Table Name: ")
# tableSpace = input("Enter the Table Space or nothing if not applicable: ")
# storage = input("Enter the Storage or nothing if not applicable: ")
forms.write(f)
query = oracleCreateTableQuery(d,None)
alter = oracleAddPrimaryKey(schema, tableName)
fullScript = oracleCreateTable(schema, tableName, tableSpace, storage, query)
dataDictionary = excelCreateDataDict(schema, tableName, d)

newFile.write(fullScript)
newFile.write("\n\n"+alter)

newDataDict.write(dataDictionary)
"""
Checks for new SF data types. I want this dictioanry fully populated, so notify us if one is missing.
"""
for x in uniqueTypes:
    if salesForceTypes.get(x) == None:
        print("Add " + x + " to the dictionary!!! Or contact the Original Dev")

        
file.close()
newFile.close()
newDataDict.close()
forms.close()
#Uncomment to use the script directly.
#Will be deleted once the App is built
#salesforceToOracleScripter()
