VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClNotPrintedIssueAction"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Function identifyTypeOfNotPrintedIssue(oldPid As String) As String
    Dim issueDAO As New ClsIssueDAO
    Dim n As String
    Dim r As String
    
    If Len(oldPid) > 0 Then
        n = issueDAO.getIssueNumber(Mid(oldPid, 2, 9) + "|" + Mid(oldPid, 11, 4) + CStr(CInt(Mid(oldPid, 15, 4))))
        If n = "ahead" Or n = "review" Then
            r = n
        End If
    End If
    identifyTypeOfNotPrintedIssue = r
End Function



Function archiveNotPrintedVersion(NotPrintedVersionFile As String, Optional publishedIssue As String, Optional publishedFileName As String) As Boolean
    Dim src  As String
    Dim dest  As String
    Dim newfile As String
    Dim r As Boolean
    
    If NotPrintedVersionFile <> "" Then
        dest = ArchiveDirStructure.getPath()
        If Not DirExist(dest) Then
            MkDir (dest)
            MkDir (ArchiveDirStructure.getMarkupFile())
            MkDir (ArchiveDirStructure.getBodyFile())
        End If
        If Len(publishedFileName) > 0 Then
            newfile = getNewNameForArchiveFile(NotPrintedVersionFile, publishedIssue, publishedFileName)
        Else
            newfile = NotPrintedVersionFile
        End If
        
        src = CurrentDirStructure.getMarkupFile(NotPrintedVersionFile)
        dest = ArchiveDirStructure.getMarkupFile(newfile)
        r = moveFile(src, dest)
        
        src = CurrentDirStructure.getBodyFile(NotPrintedVersionFile)
        dest = ArchiveDirStructure.getBodyFile(newfile)
        r = r And moveFile(src, dest)
        
    End If
    archiveNotPrintedVersion = r
End Function




Function deleteArticleNotPrintedVersion(oldPid As String, publishedIssue As String, publishedFile As String) As Boolean
    Dim mst As String
    Dim ArticleNotPrintedVersionFile As String
    Dim order As String
    
    Dim inicio As Long
    Dim fim As Long
    
    Dim NotPrintedIssueDAO As ClNotPrintedIssueDAO
     Set NotPrintedIssueDAO = New ClNotPrintedIssueDAO
    
    mst = CurrentDirStructure.getBaseFile()
    
    If NotPrintedIssueDAO.setDBData(mst, mst + ".fst", mst) Then
        
        order = Mid(oldPid, Len(oldPid) - 4)
        If Len(order) > 0 Then
            If NotPrintedIssueDAO.getArticleInfo(order, inicio, fim, ArticleNotPrintedVersionFile) Then
            Else
                If CInt(order) < 100 Then
                    Call NotPrintedIssueDAO.getArticleInfo(Mid(order, 4), inicio, fim, ArticleNotPrintedVersionFile)
                End If
                'Call NotPrintedIssueDAO.getArticleInfo(Mid(order, 4), inicio, fim, ArticleNotPrintedVersionFile)
            End If
            If inicio > 0 And fim > 0 Then
                If NotPrintedIssueDAO.deleteArticleNotPrintedVersion(inicio, fim) Then
                    Call archiveNotPrintedVersion(ArticleNotPrintedVersionFile, publishedIssue, publishedFile)
                End If
            End If
        End If
    End If
    
    deleteArticleNotPrintedVersion = True
End Function

