VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsIssueDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
Private isis As New ClIsisDll

Function getIssueNumber(Id As String) As String
    Dim n As String
    Dim q As Long
    Dim Mfns() As Long
    
    q = isis.MfnFind(Id, Mfns)
    If q = 1 Then
        n = isis.UsePft(Mfns(1), "v32")
    End If
    getIssueNumber = n
End Function
Function getIssueOrder(Id As String) As String
    Dim n As String
    Dim q As Long
    Dim Mfns() As Long
    
    q = isis.MfnFind(Id, Mfns)
    If q = 1 Then
        n = isis.UsePft(Mfns(1), "v36")
    End If
    getIssueOrder = n
End Function
Function getDocCounter(Id As String) As Long
    Dim valueTotalOfDocuments As String
    Dim totalOfDocuments As Long
    Dim q As Long
    Dim Mfns() As Long
    
    q = isis.MfnFind(Id, Mfns)
    If q = 1 Then
        valueTotalOfDocuments = isis.FieldContentOccGet(Mfns(q), BV(Currbv).BVISISTAGS("doccount").Value, 1)
        If IsNumber(valueTotalOfDocuments) Then totalOfDocuments = CLng(valueTotalOfDocuments)
    End If
    getDocCounter = totalOfDocuments
End Function

Private Sub Class_Initialize()
    Set isis = New ClIsisDll
    
    If isis.Initiate(BV(Currbv).FileTree.DirNodes("Issue Database").fullpath, BV(Currbv).FileTree.DirNodes("Issue Database").text, BV(Currbv).FileTree.DirNodes("Issue Database").key) Then
        If isis.IfCreate(BV(Currbv).FileTree.DirNodes("Issue Database").text, BV(Currbv).FileTree.DirNodes("Issue Database").key) Then
        
        End If
    End If
End Sub
