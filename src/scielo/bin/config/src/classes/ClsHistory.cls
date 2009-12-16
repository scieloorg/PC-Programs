VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsHistory"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private statusCollection As New Collection
Private statusCollection2 As New Collection

Sub add(j As ClsJournalStatus, Key As String)
    On Error Resume Next
    Call statusCollection.add(j, Key)
    Call statusCollection2.add(j, CStr(statusCollection.count))
End Sub

Function count() As Long
    count = statusCollection.count
End Function

Function item(Index As Variant) As ClsJournalStatus

    On Error Resume Next
    Set item = statusCollection.item(Index)
    If item Is Nothing Then
        Set item = statusCollection2.item(Index)
    End If
End Function

Function remove(Index As Variant) As Boolean
    Dim item2 As Object
    
    Set item2 = statusCollection.item(Index)
    If item2 Is Nothing Then
        Set item2 = statusCollection2.item(Index)
        If Not (item2 Is Nothing) Then
            Call statusCollection2.remove(Index)
        End If
    Else
        Call statusCollection.remove(Index)
    End If
    
End Function


Sub clean()
    While 0 < statusCollection.count
        statusCollection.remove (statusCollection.count)
        statusCollection2.remove (statusCollection2.count)
    Wend
End Sub
