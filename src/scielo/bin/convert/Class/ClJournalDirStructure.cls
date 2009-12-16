VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClJournalDirStructure"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Private mVarRoot As String
Private mVarJournalAcronym As String

Private mVarRelatedIssues As ClsRelatedIssues

Property Set relatedissues(x As ClsRelatedIssues)
    Set mVarRelatedIssues = x
End Property
Property Get relatedissues() As ClsRelatedIssues
    Set relatedissues = mVarRelatedIssues
End Property

Property Let serialPath(v As String)
    mVarRoot = v
End Property
Property Get serialPath() As String
    serialPath = mVarRoot
End Property

Property Let journalDir(v As String)
    mVarJournalAcronym = v
End Property
Property Get journalDir() As String
    journalDir = mVarJournalAcronym
End Property
Function getJournalPath() As String
    getJournalPath = mVarRoot + "\" + mVarJournalAcronym
End Function
Sub setDirStructure(MarkupPath As String)
    Dim Count As Long
    Dim parts() As String
    Dim i As Long
    Dim found As Boolean
    Dim s As String
    Dim sep As String
    
    sep = "\"
    parts = Split(MarkupPath, sep)
    Count = UBound(parts)
    i = Count
    While (i > 0) And (Not found)
        If parts(i) = "markup" Then
            found = True
        End If
        i = i - 1
    Wend
    
    Set relatedissues = New ClsRelatedIssues
    
    Set relatedissues.Issue = New ClIssueDirStructure
    relatedissues.Issue.issueDir = parts(i)
    
    mVarJournalAcronym = parts(i - 1)
    
    i = i - 2
    While (i >= 0)
        mVarRoot = parts(i) + s + mVarRoot
        s = sep
        i = i - 1
    Wend
    
    relatedissues.Issue.journalPath = getJournalPath()
    relatedissues.setArchive
    
  '  mVarRoot sep + mVarJournalAcronym + sep + mVarIssue + sep + markupDir + sep + file
End Sub



