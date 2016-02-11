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
Public current_status As String
Public recent_date As String


Sub add(j As ClsJournalStatus, key As String)
    On Error Resume Next
    Dim d1 As Long
    Dim d2 As Long
    
    d1 = 0
    d2 = 0
    If recent_date <> "" Then
        d1 = CLng(recent_date)
    End If
    If j.statusDate <> "" Then
        d2 = CLng(j.statusDate)
    End If
    
    If d1 < d2 Then
        recent_date = j.statusDate
        current_status = j.status
    End If
    
    Call statusCollection.add(j, key)
    Call statusCollection2.add(j, CStr(statusCollection.count))
End Sub

Function count() As Long
    count = statusCollection.count
End Function

Function item(index As Variant) As ClsJournalStatus

    On Error Resume Next
    Set item = statusCollection.item(index)
    If item Is Nothing Then
        Set item = statusCollection2.item(index)
    End If
End Function

Function remove(index As Variant) As Boolean
    Dim item2 As Object
    
    Set item2 = statusCollection.item(index)
    If item2 Is Nothing Then
        Set item2 = statusCollection2.item(index)
        If Not (item2 Is Nothing) Then
            Call statusCollection2.remove(index)
        End If
    Else
        Call statusCollection.remove(index)
    End If
    
End Function


Sub clean()
    While 0 < statusCollection.count
        statusCollection.remove (statusCollection.count)
        statusCollection2.remove (statusCollection2.count)
    Wend
End Sub
