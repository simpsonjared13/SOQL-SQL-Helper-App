import PySimpleGUI as sg from OdsScript import * path = ""

sg.theme("DarkTeal2") layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-File-")],
                                [sg.T("")], [sg.Text("Choose a Folder: "), sg.Input(), sg.FolderBrowse(key="-Folder-")], 
                                [sg.T("")], [sg.Text("Enter a Name for the New Script: "), sg.Input(key="-Script-")], [sg.T("")], 
                                [sg.Text("Enter a Name for the New Data Dictionary: "), sg.Input(key="-Dictionary-")], [sg.T("")], 
                                [sg.Text("Enter the Schema Name: "), sg.Input(key="-Schema-")], 
                                [sg.T("")], [sg.Text("Enter the Table Name: "), sg.Input(key="-Table-")], 
                                [sg.T("")], [sg.Text("Enter the Table Space or nothing if not applicable: "), sg.Input(key="-Space-")], 
                                [sg.T("")], [sg.Text("Enter the Table Storage or nothing if not applicable: "), sg.Input(key="-Storage-")], [sg.Button("Submit")]]

###Building Window window = sg.Window('My File Browser', layout, size=(600,500))

while True: 
    event, values = window.read() 
    if event == sg.WIN_CLOSED or event=="Exit":
        break 
    elif event == "Submit": 
        salesforceToOracleScripter(values["-File-"], values["-Folder-"], values["-Script-"], 
                                   values["-Dictionary-"], values["-Schema-"], values["-Table-"] , 
                                   values["-Space-"], values["-Storage-"]) 
        print("Complete, check your folders for the files") window.close()
