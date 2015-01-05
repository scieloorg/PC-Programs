VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsIssue"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Public volume As String
Public number As String
Public suppl As String
Public vsuppl As String
Public idPart As String
Public issueorder As String

Public doccount As String
Public DateISO As String
Public issuepart As String
Public issueSponsor As String
Public issuePublisher As String
Public issueCover As String

Public markupDone As String
Public status As String

Public journal As ClsJournal
Public issueTitle As ColTextByLang
Public license_code As String

Public bibstrips As ColObjByLang
Public toc As ClsTOC
Public eissn As String
Public pissn As String


         
Function issueId() As String
    Dim x As String
    
    If volume <> "" Then
        x = x + "v" + volume
    End If
    If vsuppl <> "" Then
        x = x + "s" + vsuppl
    End If
    If number <> "" Then
        x = x + "n" + number
    End If
    If suppl <> "" Then
        x = x + "s" + suppl
    End If
    If idPart <> "" Then
        x = x + idPart
    End If
    issueId = x + " " + issueorder
End Function

Private Sub Class_Initialize()
    Set journal = New ClsJournal
    Set toc = New ClsTOC
    Set issueTitle = New ColTextByLang
    Set bibstrips = New ColObjByLang
    Set bibstrips.nullObject = New ClsBibStrip
    
End Sub
