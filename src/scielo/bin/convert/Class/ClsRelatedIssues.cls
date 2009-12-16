VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsRelatedIssues"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Private mVarIssue As New ClIssueDirStructure
Private mvarArchive As ClIssueDirStructure
'Private mVarPrevious As ClsRelatedIssues
Private rules As New ClsIssueDirNameRules

Property Set archive(x As ClIssueDirStructure)
    Set mvarArchive = x
End Property
Property Get archive() As ClIssueDirStructure
    Set archive = mvarArchive
End Property

Property Set Issue(x As ClIssueDirStructure)
    Set mVarIssue = x
End Property
Property Get Issue() As ClIssueDirStructure
    Set Issue = mVarIssue
End Property

'Property Set Previous(x As ClsRelatedIssues)
    'Set mVarPrevious = x
'End Property
'Property Get Previous() As ClsRelatedIssues
 '   Set Previous = mVarPrevious
'End Property


Function setArchive() As Boolean
    Dim year As String
    If rules.identifyIssueType(Issue.issueDir, year) <> "" Then
        Set archive = New ClIssueDirStructure
        archive.issueDir = rules.createIssueDir(rules.identifyIssueType(Issue.issueDir, year), year, True)
        archive.journalPath = Issue.journalPath
    End If
    setArchive = True
End Function

Function identifyIssueType() As String
    identifyIssueType = rules.identifyIssueType(Issue.issueDir)
End Function

Function archiveFile(currFileName As String, oldFileName As String) As Boolean
  
    Dim newfile As String
    Dim src As String
    Dim dest As String
    Dim r As Boolean
    
    If Not DirExist(archive.getIssuePath()) Then
        MakeDir (archive.getIssuePath())
    End If
    If Not DirExist(archive.getMarkupFile()) Then
        MakeDir (archive.getMarkupFile())
    End If
    If Not DirExist(archive.getBodyFile()) Then
        MakeDir (archive.getBodyFile())
    End If
    If Len(currFileName) > 0 Then
        newfile = getNewNameForArchiveFile(oldFileName, currFileName)
    Else
        newfile = oldFileName
    End If
    
    src = Issue.getMarkupFile(oldFileName)
    dest = archive.getMarkupFile(newfile)
    r = moveFile(src, dest)
    
    src = Issue.getBodyFile(oldFileName)
    dest = archive.getBodyFile(newfile)
    r = r And moveFile(src, dest)
    
    archiveFile = r
End Function

Private Function getNewNameForArchiveFile(currName As String, publishedFileName As String) As String
    getNewNameForArchiveFile = Mid(currName, 1, InStrRev(currName, ".htm") - 1) + "_aka_" + Issue.issueDir + "_" + publishedFileName
End Function
