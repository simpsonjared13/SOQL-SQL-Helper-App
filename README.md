# app
salesforcescript
String objectName = 'ObjectAPIName';
//You must change the object API name in the following line to get info!!!
Map<String, Schema.SObjectField> fieldMap = Schema.SObjectType.ObjectAPIName.fields.getMap();
//Schema.SObjectField test = fieldMap.get('Client_Segment__c');
//System.debug(test.getDescribe());
String message ='';// + test.getDescribe();
for(Schema.SObjectField sof : fieldMap.values()){
    Schema.DescribeFieldResult dfr = sof.getDescribe();
    message+= 'Name:'+ dfr.getName() + ', Type:' + dfr.getType() + ', Length:' 
                 + dfr.getLength() + ', Precision:' + dfr.getPrecision()
                + ', Default Value:' + dfr.getDefaultValue() +
        	+ ', Scale:' + dfr.getScale() + ', Digits:' + dfr.getDigits() +
    		+ ', Unique:' + dfr.isUnique() + ', AutoNumber:' + dfr.isAutoNumber()
        	+ ', Label:' + dfr.getLabel() + ', Formula:' + dfr.isCalculated();
    message+='\n';
}		
//System.debug(message);
Messaging.reserveSingleEmailCapacity(1);
Messaging.SingleEmailMessage mail = new Messaging.SingleEmailMessage();
String[] toAddresses = new String[] {'example@email.com'}; 
mail.setToAddresses(toAddresses);
mail.setSubject('' + objectName + ' Details');
mail.setPlainTextBody(message);
Messaging.sendEmail(new Messaging.SingleEmailMessage[] { mail });


odsscript
from OdsHelper import *

def salesforceToOracleScripter(path,folder,scriptName,dictionaryName,schema,tableName,tableSpace,storage):
    """
    Declare Variables
    """
    # path = input("Enter the file path of the file to read: ")
    # fileToRead = input("Enter the file name without .txt: ")

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
# Uncomment to use the script directly.
# Will be deleted once the App is built
#salesforceToOracleScripter()


OdsHelper
typeDictionary = {'ID': 'ID', 'BOOLEAN': 'BOOLEAN', 'STRING': 'STRING', 'REFERENCE': 'REFERENCE', 'DATETIME': 'DATETIME',
                  'DATE': 'DATE', 'MULTIPICKLIST': 'MULTIPICKLIST', 'DOUBLE': 'DOUBLE', 'PICKLIST': 'PICKLIST',
                  'TEXTAREA': 'TEXTAREA', 'TIME': 'TIME', 'CURRENCY': 'CURRENCY', 'EMAIL': 'EMAIL', 'PERCENT': 'PERCENT'}
def getSalesForceTypes():
    return typeDictionary

# Creates the SQL Query to Create a table
def oracleCreateTable(schema, tableName, tableSpace, storage, query):
    if schema == None or tableName == None:
        return "Error! Schema, TableName or TableSpace were not provided!!!"
    fullScript = "CREATE TABLE " + schema + "." + tableName + " \n(" + query 
    #Close the Table Creation Query
    fullScript += ")"

    if tableSpace:
        fullScript += " TABLESPACE " + tableSpace
    if storage:
        fullScript += " STORAGE " + "(" + storage + ")"
    fullScript += ";"
    return fullScript

def oracleAddPrimaryKey(schema, tableName):
    query = "ALTER TABLE " + schema +"." + tableName + " ADD ("
    query+= "CONSTRAINT " + tableName + "_PK PRIMARY KEY (Id) ENABLE VALIDATE);"
    return query

# Creates the dynamic portion of a CREATE TABLE SQL Query 
def oracleCreateTableQuery(dictionary, timezone):
    string=""
    count = 0
    length = len(dictionary)
    for key in dictionary:
        count+=1
        valueList = dictionary[key]
        dataType = valueList[0]
        string+= key + " "
        """ Creates the Inner Query """
        if dataType == 'ID':
            string+= "NVARCHAR2(" + valueList[1] + ") NOT NULL"
        elif dataType == "BOOLEAN":
            string+= "NVARCHAR2(1)"
        elif dataType == "DATE":
            string+= "DATE"
        elif dataType == "DATETIME":
            # if timezone != None:
                string+= "DATE"
            # else: 
            #     string+= "TIMESTAMP(0)"
        elif dataType == "TIME":
            string+= "NVARCHAR2(50) "
        elif dataType == 'DOUBLE' or dataType =='PERCENT' or dataType == 'CURRENCY':
            string+=  "NUMBER(" + valueList[1] + "," + valueList[2] + ")"
            if valueList[3] != "null":
                string+= " NOT NULL"
        else:
            if int(valueList[1]) > 1300:
                string+= "NVARCHAR2(1300)"
            else:
                string+= "NVARCHAR2(" + valueList[1] + ")"
            if valueList[2] != "null":
                string+= " NOT NULL"
        """ Adds a comma if there are more fields to add """
        if count != length:
            string+=",\n"
    return string

#def excelCreateDataDict(schema, tableName, tableSpace, storage, dictionary, timezone):
def excelCreateDataDict(schema, tableName, dictionary):
    string="API Name,Field Label,Table Name,Column Name,Column Definition,Column Datatype,Nullable,Is PK,Masked,Formula\n"
    count = 0
    length = len(dictionary)
    for key in dictionary:
        count+=1
        valueList = dictionary[key]
        dataType = valueList[0]
        if dataType == "DOUBLE" or dataType =="PERCENT" or dataType == "CURRENCY":
            salesforceLabel = valueList[4]
            isNull = valueList[3]
        else:
            salesforceLabel = valueList[3]
            isNull = valueList[2]
        string+= key + ";" + salesforceLabel+ ";" + tableName + ";" + str(key).upper() + "; ;"
        """ Creates the Inner Query """
        if dataType == 'ID':
            string+= "NVARCHAR2(" + valueList[1] + ")"
        elif dataType == "BOOLEAN":
            string+= "NVARCHAR2(1)"
        elif dataType == "DATE":
            string+= "DATE"
        elif dataType == "DATETIME":
            # if timezone != None:
                string+= "DATE"
            # else: 
            #     string+= "TIMESTAMP(0)"
        elif dataType == "TIME":
            string+= "NVARCHAR2(50) "
        elif dataType == 'DOUBLE' or dataType =='PERCENT' or dataType == 'CURRENCY':
            string+=  "NUMBER(" + valueList[1] + "," + valueList[2] + ")"
            if valueList[3] != "null":
                string+= "NOT NULL"
        else:
            if int(valueList[1]) > 1300:
                string+= "NVARCHAR2(1300)"
            else:
                string+= "NVARCHAR2(" + valueList[1] + ")"
            if valueList[2] != "null":
                string+= "NOT NULL"
        """ Adds a comma if there are more fields to add """
        #if count != length:
        string+=";" + isNull + ";"
        if dataType == 'ID':
            string+= "Yes"
        else:
            string += "No"
        string+="\n"
    return string

GUI
import PySimpleGUI as sg
from OdsScript import *
path = ""

sg.theme("DarkTeal2")
layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-File-")], 
    [sg.T("")], [sg.Text("Choose a Folder: "), sg.Input(), sg.FolderBrowse(key="-Folder-")],
    [sg.T("")], [sg.Text("Enter a Name for the New Script: "), sg.Input(key="-Script-")],
    [sg.T("")], [sg.Text("Enter a Name for the New Data Dictionary: "), sg.Input(key="-Dictionary-")],
    [sg.T("")], [sg.Text("Enter the Schema Name: "), sg.Input(key="-Schema-")],
    [sg.T("")], [sg.Text("Enter the Table Name: "), sg.Input(key="-Table-")],
    [sg.T("")], [sg.Text("Enter the Table Space or nothing if not applicable: "), sg.Input(key="-Space-")],
    [sg.T("")], [sg.Text("Enter the Table Storage or nothing if not applicable: "), sg.Input(key="-Storage-")],
    [sg.Button("Submit")]]

###Building Window
window = sg.Window('My File Browser', layout, size=(600,500))
    
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        salesforceToOracleScripter(values["-File-"], values["-Folder-"], values["-Script-"], values["-Dictionary-"], values["-Schema-"], values["-Table-"]
            , values["-Space-"], values["-Storage-"])
        print("Complete, check your folders for the files")
window.close()


triggerhandler
 * Originally by Kevin O'Hara github.com/kevinohara80/sfdc-trigger-framework
