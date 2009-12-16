VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsArticle"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
Private mvarOrder As String
Private mvarFilename As String
Private mvarMfn As String
Private mvarVersionHistory As ClsArticleVersionHistory
Private mvartitle As String
Private mvarsurname As String
Private mvarIssueNo As String
Private mvarIssn As String
Private mvarDateISO As String

Private mvarIsArchived As Boolean


Private mvarissueOrder As String

Public Property Get issueOrder() As String
    issueOrder = mvarissueOrder
End Property

Public Property Let issueOrder(ByVal vNewValue As String)
    mvarissueOrder = vNewValue
End Property



Public Property Get IsArchived() As Boolean
    IsArchived = mvarIsArchived
End Property

Public Property Let IsArchived(ByVal vNewValue As Boolean)
    mvarIsArchived = vNewValue
End Property

Public Property Get Mfn() As String
    Mfn = mvarMfn
End Property

Public Property Let Mfn(ByVal vNewValue As String)
    mvarMfn = vNewValue
End Property

Public Property Get order() As String
    order = mvarOrder
End Property

Public Property Let order(ByVal vNewValue As String)
    mvarOrder = vNewValue
End Property

Public Property Get FileName() As String
FileName = mvarFilename
End Property

Public Property Let FileName(ByVal vNewValue As String)
mvarFilename = vNewValue
End Property

Public Property Get VersionHistory() As ClsArticleVersionHistory
Set VersionHistory = mvarVersionHistory
End Property

Public Property Set VersionHistory(ByVal vNewValue As ClsArticleVersionHistory)
Set mvarVersionHistory = vNewValue
End Property

Public Property Get surname() As String
    surname = mvarsurname
End Property

Public Property Let surname(ByVal vNewValue As String)
    mvarsurname = vNewValue
End Property
Public Property Get title() As String
    title = mvartitle
End Property

Public Property Let title(ByVal vNewValue As String)
    mvartitle = vNewValue
End Property

    
Public Property Get IssueNo() As String
    IssueNo = mvarIssueNo
End Property

Public Property Let IssueNo(ByVal vNewValue As String)
    mvarIssueNo = vNewValue
End Property

    Public Property Get dateiso() As String
    dateiso = mvarDateISO
End Property

Public Property Let dateiso(ByVal vNewValue As String)
    mvarDateISO = vNewValue
End Property

    Public Property Get issn() As String
    issn = mvarIssn
End Property

Public Property Let issn(ByVal vNewValue As String)
    mvarIssn = vNewValue
End Property

Function isValidPreviousArticle() As Boolean
    Dim r As Boolean
    r = True
    
    r = r And Len(FileName) > 0
    r = r And Len(order) > 0
    r = r And ((Len(VersionHistory.AHP_PID) > 0 Or Len(VersionHistory.AHPDate) > 0) Or (Len(VersionHistory.RVP_PID) > 0 Or Len(VersionHistory.RVPDate) > 0))
    r = r And Len(pid) = 23
    r = r And Len(IssueNo) > 0
    r = r And Len(dateiso) > 0
    isValidPreviousArticle = r
End Function


Function pid() As String
    Dim t As String
    
    Dim v As String
    
    t = "00000" + order
    t = Mid(t, Len(t) - 5 + 1)
               
    v = "0000" + Mid(issueOrder, 5)
    v = Mid(v, Len(v) - 4 + 1)
    
    pid = "S" + issn + Mid(dateiso, 1, 4) + v + t
    
End Function
