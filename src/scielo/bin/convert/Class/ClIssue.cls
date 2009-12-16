VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClCfgRec"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Function ImportIssueRecord(IssueId As String) As Boolean
    Dim BD As ClDBDoc
    Dim ret As Boolean
    Dim q As Long
    Dim MfnIssue() As Long
    Dim DBIssue  As ClIsisDll
    
    Set BD = New ClDBDoc
    Set DBIssue = New ClIsisDll
    Set DBIssue = LoadIsisDB("Issue Database", ret)
    If ret Then
        If BD.Inicia(PathBase, ArqBase, FormMenu.DirStruct.Nodes("Database Directory").key) Then
            q = DBIssue.MfnFind(IssueId, MfnIssue)
            If q > 0 Then
                ret = BD.ConfigRecordSave(DBIssue.RecordGet(MfnIssue(q)))
            ElseIf q = 0 Then
                Call Msg.GiveRunInformation("Configuration record is missing in database Issue.", True)
            End If
        End If
    End If
    Set DBIssue = Nothing
    Set BD = Nothing
    ImportIssueRecord = ret
End Function

Function CheckDocCount() As Long
    Dim BD As ClDBDoc
    Dim ret As Long
        
    Set BD = New ClDBDoc
    If BD.Inicia(PathBase, ArqBase, FormMenu.DirStruct.Nodes("Database Directory").key) Then
        ret = BD.DocCounter
    End If
    Set BD = Nothing
    CheckDocCount = ret
End Function

Function IssueId(vol As String, supplvol As String, Num As String, SupplNum As String) As String
    Dim ret As String
    
    If Len(vol) > 0 Then ret = ret + VOLSGL + vol
    If Len(supplvol) > 0 Then ret = ret + VOLSUPPLSGL + supplvol
    If Len(Num) > 0 Then ret = ret + NOSGL + Num
    If Len(SupplNum) > 0 Then ret = ret + NOSUPPLSGL + SupplNum
    
    IssueId = ret
End Function

Function IssueKey(vol As String, supplvol As String, Num As String, SupplNum As String) As String
    Dim ret As String
    
    ret = ret + VOLSGL + vol
    ret = ret + VOLSUPPLSGL + supplvol
    ret = ret + NOSGL + Num
    ret = ret + NOSUPPLSGL + SupplNum
    
    IssueKey = ret
End Function

Function MsgIssueId(vol As String, supplvol As String, Num As String, SupplNum As String, Iseqno As String) As String
    Dim ret As String
    
    If Len(vol) > 0 Then ret = ret + "Volume = " + vol + vbCrLf
    If Len(supplvol) > 0 Then ret = ret + "Volume Suppl = " + supplvol + vbCrLf
    If Len(Num) > 0 Then ret = ret + "Number = " + Num + vbCrLf
    If Len(SupplNum) > 0 Then ret = ret + "Number Suppl = " + SupplNum + vbCrLf
    If Len(Iseqno) > 0 Then ret = ret + "Seq. Number = " + Iseqno + vbCrLf
    MsgIssueId = ret
End Function


