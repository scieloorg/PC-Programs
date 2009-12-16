VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClMsg"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public WarningFile As String

'-----------------------------------------------------------------------
'WriteLogFile - escreve os passos do processamento em arquivo
'msg    - a mensagem a ser gravada no arquivo
'-----------------------------------------------------------------------
Private Sub WriteLogFile(File As String, ByVal Msg As String)
    Dim fnLog As Long
        
    fnLog = FreeFile(1)
    Open File For Append As fnLog
    Print #fnLog, Msg
    Close fnLog
End Sub

'-----------------------------------------------------------------------
'MsgInvalidPath - mensagem de caminho inválido
'Label  - identificação do caminho
'Path    - caminho
'-----------------------------------------------------------------------
Sub MsgInvalidPath(label As String, Path As String)
    MsgBox (label + " - Invalid path " + Path)
End Sub

'-----------------------------------------------------------------------
'GiveRunInformation - escreve os passos do processamento em arquivo, em msgbox e no rodapé do form
'Msg - a mensagem a ser gravada no arquivo
'ShowMsgbox - se a mensagem deve ser também mostrada ou não em msgbox
'ShowLabel  - se a mensagem deve ser também mostrada ou não em label
'-----------------------------------------------------------------------
Sub GiveRunInformation(Msg As String, Optional ShowMsgbox As Boolean, Optional ShowLabel As Boolean)
    Dim File As String
    
    If Len(WarningFile) = 0 Then
        File = "warnings.txt"
    Else
        File = WarningFile
    End If
    
    If Len(Msg) > 0 Then
        Call WriteLogFile(File, CStr(Date) + " " + CStr(Time) + " " + Msg)
        If ShowMsgbox Then MsgBox Msg
        'If ShowLabel Then ShowMsgInForm (Msg)
    Else
        Call WriteLogFile(File, "")
        'If ShowLabel Then ShowMsgInForm (Msg)
    End If
End Sub

