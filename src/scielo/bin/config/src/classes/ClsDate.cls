VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsDate"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Function formatDate(mvarLang As String, mvarDate As String) As String
    Dim x As String
    Select Case mvarLang
    Case "pt"
        x = Mid(mvarDate, 7, 2) + "/" + Mid(mvarDate, 5, 2) + "/" + Mid(mvarDate, 1, 4)
    Case "es"
        x = Mid(mvarDate, 7, 2) + "/" + Mid(mvarDate, 5, 2) + "/" + Mid(mvarDate, 1, 4)
    Case "en"
        x = Mid(mvarDate, 5, 2) + "/" + Mid(mvarDate, 7, 2) + "/" + Mid(mvarDate, 1, 4)
    End Select
    formatDate = x
End Function

Function getDateIso(mvarLang As String, formatedDate As String) As String
    Dim mvarDate As String
    Select Case mvarLang
    Case "pt"
        mvarDate = Mid(formatedDate, 7, 4) + Mid(formatedDate, 4, 2) + Mid(formatedDate, 1, 2)
    Case "es"
        mvarDate = Mid(formatedDate, 7, 4) + Mid(formatedDate, 4, 2) + Mid(formatedDate, 1, 2)
    Case "en"
        mvarDate = Mid(formatedDate, 7, 4) + Mid(formatedDate, 1, 2) + Mid(formatedDate, 4, 2)
    End Select
getDateIso = mvarDate
End Function
