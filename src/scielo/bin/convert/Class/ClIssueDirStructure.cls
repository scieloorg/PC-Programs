VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClIssueDirStructure"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Const baseDir = "base"
Const markupDir = "markup"
Const bodyDir = "body"
Const sep = "\"

Private mVarIssue As String
Private mVarJournalPath As String
Private mvarIssueType As String

Property Let issueDir(v As String)
    mVarIssue = v
End Property
Property Get issueDir() As String
    issueDir = mVarIssue
End Property
Property Let journalPath(v As String)
    mVarJournalPath = v
End Property
Property Get journalPath() As String
    journalPath = mVarJournalPath
End Property
Function getIssuePath() As String
    getIssuePath = journalPath + sep + mVarIssue
End Function
Function getMarkupFile(Optional File As String) As String
    getMarkupFile = getIssuePath + sep + markupDir + sep + File
End Function
Function getBodyFile(Optional File As String) As String
    getBodyFile = getIssuePath + sep + bodyDir + sep + File
End Function
Function getBaseFile() As String
    getBaseFile = getIssuePath + sep + baseDir + sep + mVarIssue
End Function
Function getBasePath() As String
    getBasePath = getIssuePath + sep + baseDir
End Function
Function getBaseFileName() As String
    getBaseFileName = mVarIssue
End Function

'Public Property Get issueType() As Variant
'    issueType = mvarIssueType
'End Property

'Public Property Let issueType(ByVal vNewValue As Variant)
'    mvarIssueType = vNewValue
'End Property


