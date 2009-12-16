VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClArchiveDirStructure"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Private mvarArchiveDirStructure As ClIssueDirStructure

Public Property Get ArchiveDirStructure() As ClIssueDirStructure
    Set ArchiveDirStructure = mvarArchiveDirStructure
End Property

Public Property Set ArchiveDirStructure(ByVal vNewValue As ClIssueDirStructure)
    Set mvarArchiveDirStructure = vNewValue
End Property

Private Function setData(typeOfIssue As String, Path As String, Year As String) As Boolean
    typeOfNotPrintedIssue = typeOfIssue
    
    If typeOfIssue = "ahead" Or typeOfIssue = "review" Then
        Set ArchiveDirStructure = New ClIssueDirStructure
        
        If Len(Year) > 0 Then
            ArchiveDirStructure.issueDir = Year + typeOfIssue + "_archive"
        Else
            ArchiveDirStructure.issueDir = "ex-" + typeOfIssue
        End If
        ArchiveDirStructure.journalPath = Path
        setData = True
    End If
    
End Function
Function init(issueDir As String, journalPath As String) As Boolean
    typeOfIssue = testeType(issueDir, "ahead", Year)
    If Len(typeOfIssue) = 0 Then typeOfIssue = testeType(issueDir, "review", Year)
    Call setData(typeOfIssue, journalPath, Year)
    
End Function
        
Private Function testeType(issueDir As String, IssueType As String, Year As String) As String
    Dim r As String
    Dim p As String
    
    p = InStr(issueDir, IssueType)
    If p > 0 Then
        r = IssueType
    End If
    If p > 2 Then
        Year = Mid(issueDir, 1, 4)
    End If
    testeType = r
End Function
