VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsIsisField"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private subFields As New ClsParams


Public Function update(subf As String, val As String) As Boolean
    If subFields.item(subf) <> "" Then
        subFields.add val, subf
    Else
        subFields.item(subf) = val
    End If
    update = True
End Function

