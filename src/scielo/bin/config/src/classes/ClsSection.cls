VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsSection"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Public sectionNames As New ColTextByLang
Public sectionCode As String

Function getNames() As String
    Dim x As String
    Dim i As Long
    
    For i = 1 To sectionNames.count
        x = x + sectionNames.getItemByIndex(i).text
    Next
    getNames = x
End Function
