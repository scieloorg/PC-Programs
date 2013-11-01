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
    Dim f As String
    Dim p As String
    
    
    Open App.path & "\start.mds" For Input As #1
    Input #1, path
    Close #1
    
    Open App.path & "\p.mds" For Input As #1
    Input #1, param, paramOpen
    Input #1, param, paramProgram
    Input #1, param, paramParameters
    Input #1, param, paramDirectory
    Close #1

    
    path = LCase(path)
    f = Mid(path, InStrRev(path, "\") + 1)
    p = Mid(path, 1, InStrRev(path, "\") - 1)
    
    fn = FreeFile
    Open App.path & "\temp\openmarkup.log" For Output As #fn
    Print #fn, "path start=" & path
    Print #fn, "f=" & f
    Print #fn, "p=" & path
    Close #fn
    
    If LCase(Dir(path)) = f Then
        'executa o WORD97 com a macro q prepara ambiente de marcação
        ret = callWord(path, paramOpen, f, paramParameters, p)
    Else
        DepePath.Text1.Text = path
        DepePath.Show
    End If
    Set conf = Nothing
End Sub
Function test_start(path As String) As String

End Function
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



