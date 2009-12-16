VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsDictionary"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private col As New Collection

Sub add(v As ClsTerm, k As String)
    Call col.add(v, k)
    
End Sub

Function count() As Long
    count = col.count
End Function

Function item(k As Variant) As ClsTerm
    On Error GoTo RETORNA
    Set item = col.item(k)
    Exit Function
RETORNA:
    
    Set item = Nothing
End Function
