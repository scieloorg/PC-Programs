VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsJournalList"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Private colKey As New Collection
Private colIndex As New Collection
Sub add(journal As ClsJournal)
    On Error Resume Next
    Call colKey.add(journal, journal.key)
    Call colIndex.add(journal, CStr(colIndex.count + 1))
End Sub

Function count() As Long
    count = colKey.count
End Function

Function getItemByKey(key As String) As ClsJournal
    Set getItemByKey = colKey.item(key)
End Function
Function getItemByIndex(i As Long) As ClsJournal
    Set getItemByIndex = colIndex.item(i)
End Function


