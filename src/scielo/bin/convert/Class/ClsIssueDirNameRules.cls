VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsIssueDirNameRules"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Function identifyIssueType(issueDir As String, Optional year As String) As String
    Dim r As String
    
    If Mid(issueDir, Len(issueDir) - 1, 2) = "pr" Then
        r = ""
    ElseIf InStr(issueDir, "ahead") > 0 Then
        r = "ahead"
        If Len(issueDir) > Len("ahead") + 1 Then
            year = Mid(issueDir, 1, 4)
        End If
    ElseIf InStr(issueDir, "review") > 0 Then
        r = "review"
        If Len(issueDir) > Len("review") + 1 Then
            year = Mid(issueDir, 1, 4)
        End If
    Else
        r = ""
    End If
    If IsNumber(year) Then
    If CInt(year) <= 2007 Then
        year = ""
    End If
    End If
    identifyIssueType = r
End Function
Function createIssueDir(issueType As String, year As String, forArchive As Boolean) As String
    If IsNumber(year) Then
        If CInt(year) > 2007 Then
            createIssueDir = year + "n" + issueType
        Else
            createIssueDir = "n" + issueType
        End If
    Else
        createIssueDir = "n" + issueType
    End If
    If forArchive Then
        createIssueDir = "ex-" + createIssueDir
    End If
End Function

Function identifyPreviousIssueData(issueType As String, RVPDate As String, AHPDate As String, outIssue As String, outYear As String) As Boolean
    Select Case issueType
    Case "review"
        
    Case "ahead"
        If Len(RVPDate) > 0 Then
            outYear = Mid(RVPDate, 1, 4)
            outIssue = "review"
        End If
    Case Else
        If Len(AHPDate) > 0 Then
            outIssue = "ahead"
            outYear = Mid(AHPDate, 1, 4)
        Else
            If Len(RVPDate) > 0 Then
                outYear = Mid(RVPDate, 1, 4)
                outIssue = "review"
            End If
        End If
    End Select
    If IsNumber(outYear) Then
        If CInt(outYear) <= 2007 Then
        outYear = ""
        End If
    End If
    identifyPreviousIssueData = (Len(outIssue) > 0)
End Function
