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
Public licenses As ColTextByLang
Public bibstrips As ColObjByLang
Public toc As ClsTOC
Private mvarISSN As String
Public Property Get issueISSN() As Variant
    issueISSN = mvarISSN
End Property

Public Property Let issueISSN(ByVal vNewValue As Variant)
    mvarISSN = vNewValue
End Property


         
Function issueId() As String
    Dim X As String
    
    If volume <> "" Then
        X = X + "v" + volume
    End If
    If vsuppl <> "" Then
        X = X + "s" + vsuppl
    End If
    If number <> "" Then
        X = X + "n" + number
    End If
    If suppl <> "" Then
        X = X + "s" + suppl
    End If
    If idPart <> "" Then
        X = X + idPart
    End If
    issueId = X + " " + issueorder
End Function

Private Sub Class_Initialize()
    Set journal = New ClsJournal
    Set toc = New ClsTOC
    Set issueTitle = New ColTextByLang
    Set licenses = New ColTextByLang
    Set bibstrips = New ColObjByLang
    Set bibstrips.nullObject = New ClsBibStrip
    
End Sub
