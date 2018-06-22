Set objShell = CreateObject("Wscript.Shell")

' Getting the folder where the script is running
strPath = Wscript.ScriptFullName
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.GetFile(strPath)
strFolder = objFSO.GetParentFolderName(objFile) 

' Running the game setup
strPath = strFolder & "/Scripts/assert_files.pyw"
objShell.Run strPath

' Checking if the game is ready to be run
Set fso = CreateObject("Scripting.FileSystemObject")
AssertSafe = strFolder & "\Saves\General info\clear run.txt"
Set file = fso.OpenTextFile(AssertSafe)
validation = file.ReadAll

if validation = "True" then
    gamePath = strFolder & "/main_game.py"
    objShell.Run gamePath
else
    error = fso.OpenTextFile(strFolder & "\Saves\General info\errors.txt").ReadAll
    msgbox error
end if
