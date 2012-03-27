VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsJournalTOCManager"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private xMfnSection As Long
Private xJournalInfo As ClsJournal
Private journalTOC As ClsTOC
Private sectionDAO As New ClsSectionDAO



Public Function create(j As ClsJournal)
    Set xJournalInfo = j
    
    
    With Paths("Section Database")
        Call sectionDAO.create(.Path, .FileName, .key)
    End With
        
    
    
    
Set journalTOC = sectionDAO.getTOC(j.Title, j.ISSN, j.pubid, xMfnSection)
    If journalTOC Is Nothing Then
    Else
        journalTOC.loadDict
    End If
    End Function

Property Get toc() As ClsTOC
    Set toc = journalTOC
End Property
Property Set toc(t As ClsTOC)
    Set journalTOC = t
    journalTOC.loadDict
End Property

Public Function whereSectionInUse(code As String, resultType As String, issues As ClsIssues) As Boolean
    Dim issueDAO As ClsIssueDAO
    
    With Paths("Issue Database")
    Set issueDAO = New ClsIssueDAO
    Call issueDAO.create(.Path, .FileName, .key)
    End With
    
    whereSectionInUse = issueDAO.whereSectionInUse(xJournalInfo.pubid, code, issues, resultType)
    Set issueDAO = Nothing
End Function

Public Function checkSectionTitles(code As String, titles As String, codes As String) As Boolean
    Dim x As Collection
    Dim i As Long
    Dim r As Boolean
    
    Set x = journalTOC.existSectionName(titles)
    If x Is Nothing Then
        r = True
    Else
        
        For i = 1 To x.count
            If x.item(i) = code Then
                r = True
            Else
                codes = codes + x.item(i) + "; "
            End If
        Next
    End If
    checkSectionTitles = r
End Function

Public Function compare(toc1 As ClsTOC, toc2 As ClsTOC) As Boolean
    
    compare = (sectionDAO.section_TOC_DAO.tagTOC(toc1) = sectionDAO.section_TOC_DAO.tagTOC(toc2))
End Function

Public Function save() As Boolean
    save = sectionDAO.save(xJournalInfo, journalTOC, xMfnSection)
End Function
