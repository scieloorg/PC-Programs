VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColObjByLang"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private colKey As New Collection
Private colIndex As New Collection

Public nullObject As Object

Sub add(ObjByLang As Object)
    Call colKey.add(ObjByLang, ObjByLang.lang)
    Call colIndex.add(ObjByLang, CStr(colIndex.count + 1))
End Sub

Function count() As Long
    count = colKey.count
End Function

Function getItemByLang(lang As String) As Object
    On Error GoTo RETORNA
    Set getItemByLang = colKey.item(lang)
    Exit Function
RETORNA:

    
    Set getItemByLang = nullObject
End Function
Function getItemByIndex(i As Long) As Object
    On Error GoTo RETORNA
    Set getItemByIndex = colIndex.item(i)
    Exit Function
RETORNA:
    
    Set getItemByIndex = Nothing
End Function

