VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsJournalDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private isis As ClIsisdll


Function getHistory(Mfn As Long) As ClsHistory
    Dim q As Long
    Dim occs() As String
    Dim i As Long
    Dim journalStatus As ClsJournalStatus
    Dim history As New ClsHistory
    
    
    
    q = isis.FieldContentGetAll(Mfn, 51, occs)
    For i = q To 1 Step -1
        Set journalStatus = New ClsJournalStatus
        
        journalStatus.statusDate = Mid(occs(i), 3, 8)
        journalStatus.status = Mid(occs(i), 13, 1)
        
        Call history.add(journalStatus, journalStatus.statusDate)
        
        If InStr(occs(i), "^c") > 0 Then
            Set journalStatus = New ClsJournalStatus
            journalStatus.statusDate = Mid(occs(i), 16, 8)
            journalStatus.status = Mid(occs(i), 26, 1)
            
            Call history.add(journalStatus, journalStatus.statusDate)
        End If
        
    Next
    
  
    
    Set getHistory = history
End Function
Function tagHistory(history As ClsHistory) As String
    Dim i As Long
    
    Dim journalStatus As ClsJournalStatus
    
    Const tag = "51"
    Dim odd As Boolean
    Dim tagged As String
    
    odd = True
    For i = history.count To 1 Step -1
        Set journalStatus = history.item(i)
        
        If odd Then
            tagged = tagged + "<" + tag + ">^a" + journalStatus.statusDate + "^b" + journalStatus.status
        Else
            tagged = tagged + "^c" + journalStatus.statusDate + "^d" + journalStatus.status
            tagged = tagged + "</" + tag + ">"
        End If
        odd = Not odd
    Next
    If Not odd Then tagged = tagged + "</" + tag + ">"
    
    tagHistory = tagged
End Function
Private Sub Class_Initialize()
    Set isis = New ClIsisdll
    
    With Paths("Title Database")
    If isis.Inicia(.path, .FileName, .Key) Then
        If isis.IfCreate(Paths("Title X ISSN Database").FileName) Then
            
        End If
    End If
    End With
End Sub

