typeDictionary = {'ID': 'ID', 'BOOLEAN': 'BOOLEAN', 'STRING': 'STRING', 'REFERENCE': 'REFERENCE', 'DATETIME': 'DATETIME',
                  'DATE': 'DATE', 'MULTIPICKLIST': 'MULTIPICKLIST', 'DOUBLE': 'DOUBLE', 'PICKLIST': 'PICKLIST',
                  'TEXTAREA': 'TEXTAREA', 'TIME': 'TIME', 'CURRENCY': 'CURRENCY', 'EMAIL': 'EMAIL', 'PERCENT': 'PERCENT'}
def getSalesForceTypes():
    return typeDictionary

# Creates the SQL Query to Create a table
def oracleCreateTable(schema, tableName, tableSpace, storage, query):
    if schema == None or tableName == None:
        return "Error! Schema, TableName or TableSpace were not provided!!!"
    fullScript = "CREATE TABLE " + schema + "." + tableName + " (" + query 
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
            string+=", "
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

