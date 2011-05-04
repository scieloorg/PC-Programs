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
    
     Open App.path & "\start.mds" For Input As #1
    Input #1, path
    Close #1

    'verifica a existência do winword.exe
    retDir = Dir(path)
    If retDir = "WINWORD.EXE" Then
        'executa o WORD97 com a macro q prepara ambiente de marcação
        
        callWord (path)
    Else
        DepePath.Text1.Text = path
        DepePath.Show
    End If
    Set conf = Nothing
End Sub

Sub callWord(WordPath As String)
    Dim fn As Long
    Dim callw As String
    
    callw = WordPath & " /l" & App.path & "\markup.prg"
    fn = FreeFile
    Open App.path & "\temp\openmarkup.log" For Output As #fn
    Print #fn, callw
    Close #fn
    
    
     'ShellExecute hwnd, "Open", lpFile, lparameters, lpDirectory, SW_SHOWMAXIMIZED
     Call ShellExecute(hwnd, "open", "winword", " /l" & App.path & "\markup.prg", Mid(WordPath, 1, InStr(WordPath, "\winword") - 1), SW_SHOWNORMAL)
     
     'hWndAccessApp , "Open", strFolder, 0, 0, SW_SHOWNORMAL

    
'    Shell callw, vbMaximizedFocus
End Sub

