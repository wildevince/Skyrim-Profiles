' Lanceur sans fenetre console (double-clic recommande pour l'interface)
Option Explicit

Dim fso, shell, root, pythonCmd, appPath, cmd, exec

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

root = fso.GetParentFolderName(WScript.ScriptFullName)
appPath = fso.BuildPath(root, "gui\app.py")

shell.CurrentDirectory = root

If CommandExists("python3") Then
    pythonCmd = "python3"
ElseIf CommandExists("python") Then
    pythonCmd = "python"
Else
    MsgBox "Python introuvable." & vbCrLf & vbCrLf & "Installe Python depuis https://python.org" & vbCrLf & "Cochez ""Add Python to PATH"".", vbCritical, "Skyrim Profiles"
    WScript.Quit 1
End If

cmd = pythonCmd & " """ & appPath & """"
shell.Run cmd, 1, False

Function CommandExists(name)
    Set exec = shell.Exec("where " & name)
    Do While exec.Status = 0
        WScript.Sleep 10
    Loop
    CommandExists = (exec.ExitCode = 0)
End Function
