Attribute VB_Name = "Marc"
Declare Function ShellExecute Lib "shell32.dll" Alias _
  "ShellExecuteA" (ByVal hwnd As Long, ByVal lpOperation _
  As String, ByVal lpFile As String, ByVal lpParameters _
  As String, ByVal lpDirectory As String, ByVal nShowCmd _
  As Long) As Long

Public Const SW_SHOWNORMAL = 1
Public Const SW_SHOWMINIMIZED = 2
Public Const SW_SHOWMAXIMIZED = 3

Sub Main()
'este módulo lê o arquivo inicia.txt, obtendo o caminho
'para encontrar o arquivo winword.exe

'caso nao encontre, pede ao usuário indicar o end. correto

    Dim retDir As String, path As String
    'Dim conf As New clsConfig
    '------------------------
    'conf.LoadPublicValues
    
    Dim paramOpen As String
    Dim paramProgram As String
    Dim paramParameters As String
    Dim paramDirectory As String
    Dim test As String
    Dim retDirExpected As String
    Dim ret As Long
    
    Open App.path & "\start.mds" For Input As #1
    Input #1, path
    Close #1
    
    Open App.path & "\p.mds" For Input As #1
    Input #1, param, paramOpen
    Input #1, param, paramProgram
    Input #1, param, paramParameters
    Input #1, param, paramDirectory
    Close #1

    'verifica a existência do winword.exe
    retDirExpected = paramProgram
    test = Mid(path, InStr(1, path, "\office", vbTextCompare) + Len("\office"))
    test = Mid(test, 1, InStr(test, "\") - 1)
    If Len(test) > 0 Then
        If CLng(test) > 11 Then
            retDirExpected = ""
        End If
    End If
    
    retDir = Dir(path)
    
    fn = FreeFile
    Open App.path & "\temp\openmarkup.log" For Output As #fn
    Print #fn, "path=" & path
    Print #fn, "retDir=" & retDir
    Print #fn, "paramProgram=" & paramProgram
    Print #fn, "retDirExpected=" & retDirExpected
    Close #fn
    
    If (LCase(retDir) = LCase(paramProgram)) Or (LCase(retDir) = LCase(retDirExpected)) Then
        'executa o WORD97 com a macro q prepara ambiente de marcação
        
        ret = callWord(path, paramOpen, paramProgram, paramParameters, paramDirectory)
        
    Else
        DepePath.Text1.Text = path
        DepePath.Show
    End If
    Set conf = Nothing
End Sub

Function callWord(WordPath As String, paramOpen As String, paramProgram As String, paramParameters As String, paramDirectory As String) As Long
    Dim fn As Long
    Dim callw As String
    
    'callw = WordPath & " /l" & App.path & "\markup.prg"
    callw = "ShellExecute " & paramOpen & " " & paramProgram & " " & "/l" & App.path & "\markup.prg" & " " & WordPath & " " & CStr(SW_SHOWNORMAL)
    fn = FreeFile
    Open App.path & "\temp\openmarkup.log" For Append As #fn
    Print #fn, callw
    Close #fn
    
    
     'ShellExecute hwnd, "Open", lpFile, lparameters, lpDirectory, SW_SHOWMAXIMIZED
     'Call ShellExecute(hwnd, paramOpen, paramProgram, paramParameters, paramDirectory, SW_SHOWNORMAL)
     callWord = ShellExecute(hwnd, paramOpen, paramProgram, " /l" & App.path & "\markup.prg", WordPath, SW_SHOWNORMAL)
     'hWndAccessApp , "Open", strFolder, 0, 0, SW_SHOWNORMAL

    
'    Shell callw, vbMaximizedFocus
End Function

