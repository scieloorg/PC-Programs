VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsFile"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Function getFileContent(File As String) As String
    Dim fn As Long
    Dim lineread As String
    Dim r As String
    
    fn = FreeFile
    Open File For Input As fn
    While Not EOF(fn)
        Line Input #fn, lineread
        r = r & lineread
    Wend
    Close fn
    getFileContent = r
End Function
