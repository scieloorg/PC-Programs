VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsArticleDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private isis As New ClIsisDll
Private myIssueOrder As String

Private docOrderManager As New ClDocOrder

Sub setData(Path As String, mst As String, Label As String)
    If isis.Initiate(Path, mst, Label) Then
        If isis.IfCreate(mst, Label) Then
            
            
        End If
    End If
End Sub

Function getDocCounter() As Long
    Dim valueTotalOfDocuments As String
    Dim totalOfDocuments As Long
    
    valueTotalOfDocuments = isis.FieldContentOccGet(1, BV(Currbv).BVISISTAGS("doccount").Value, 1)
    If IsNumber(valueTotalOfDocuments) Then totalOfDocuments = CLng(valueTotalOfDocuments)
    
    getDocCounter = totalOfDocuments
End Function

Private Function getMfnByFilename(filename As String, Mfns() As Long) As Long
    getMfnByFilename = isis.MfnFind(filename, Mfns)
End Function
Function getDocument(filename As String) As ClsArticle
    Dim q As Long
    Dim Mfns() As Long
    Dim a As ClsArticle
    
    
    q = getMfnByFilename(filename, Mfns)
    If q > 0 Then
        Set a = New ClsArticle
        With a
        .filename = isis.FieldContentOccGet(Mfns(1), COMMONISISTAGS("pii").Value, 1)
        .order = isis.FieldContentOccGet(Mfns(1), BV(Currbv).BVISISTAGS("order").Value, 1)
        
        Set .VersionHistory = New ClsArticleVersionHistory
        .VersionHistory.AHP_PID = isis.FieldContentOccGet(Mfns(1), 881, 1)
        .VersionHistory.RVP_PID = isis.FieldContentOccGet(Mfns(1), 891, 1)
        .VersionHistory.AHPDate = isis.FieldContentOccGet(Mfns(1), 223, 1)
        .VersionHistory.RVPDate = isis.FieldContentOccGet(Mfns(1), 224, 1)
        
        .issn = isis.FieldContentOccGet(Mfns(1), 35, 1)
        '.surname = .surname
        '.title = .title
        
        .Mfn = Mfns(1)
        .IssueNo = isis.FieldContentOccGet(Mfns(1), 32, 1)
        .dateiso = isis.FieldContentOccGet(Mfns(1), 65, 1)
        
        Dim issuedao As New ClsIssueDAO
        
        .issueOrder = issuedao.getIssueOrder(.issn + isis.FieldContentOccGet(Mfns(1), 4, 1))
    
        End With
        Set getDocument = a
    End If
End Function
Private Function getDocumentRange(filename As String, inicio As Long, fim As Long) As Boolean
    Dim q As Long
    Dim Mfns() As Long
    Dim qtdDocRecords As String
    
    q = getMfnByFilename(filename, Mfns)
    If q > 0 Then
        inicio = Mfns(1) - 1
        
        qtdDocRecords = CLng(isis.FieldContentOccGet(inicio, 703, 1))
        fim = inicio + qtdDocRecords - 1
    End If
    getDocumentRange = (inicio > 0 And inicio < fim)
End Function

'XXCHECKXX
Private Function getMfnByOrder(order As String, Mfns() As Long) As Long
'Verifica se o order pertence a outro documento
    Dim Count As Long
    Dim formattedOrders() As String
    
    Dim i As Long
    Dim a As New ClsArticle
    Dim q As Long
    Dim found As Boolean
        
    i = 0
    formattedOrders = docOrderManager.getFormattedOrders(order, Count)
    
    While (Not found) And (i < Count)
        i = i + 1
        
        q = isis.MfnFind(formattedOrders(i), Mfns)
        If q > 0 Then
            found = True
        End If
    Wend
    getMfnByOrder = q
End Function
Function getDocumentByOrder(order As String) As ClsArticle
    Dim a As New ClsArticle
    Dim Mfns() As Long
    Dim q As Long
    
    q = getMfnByOrder(order, Mfns)
    If q > 0 Then
        a.filename = isis.FieldContentOccGet(Mfns(1), COMMONISISTAGS("pii").Value, 1)
        a.order = isis.FieldContentOccGet(Mfns(1), BV(Currbv).BVISISTAGS("order").Value, 1)
    End If
    Set getDocumentByOrder = a
End Function
Function getIssueOrder(issn As String, IssueId As String) As String

    Dim issuedao As New ClsIssueDAO
    
    
    getIssueOrder = issuedao.getIssueOrder(issn + IssueId)
    
End Function

Property Get issueOrder() As String
    issueOrder = myIssueOrder
End Property
Property Let issueOrder(v As String)
    myIssueOrder = v
End Property

Private Sub Class_Initialize()
    Set isis = New ClIsisDll
    docOrderManager.OrderLengthArray = BV(Currbv).getDocOrderLen(-1)
End Sub

Function Delete(filenameOrOrder As String) As Boolean
    Dim inicio As Long
    Dim fim As Long
    Dim r As Boolean
    
    If getDocumentRange(filenameOrOrder, inicio, fim) Then
        r = isis.deleteRecordRange(inicio, fim)
    End If
    Delete = r
End Function


Function ImportRecord(record As String, filename As String, order As String) As Boolean
    Dim q As Long
    Dim Mfns() As Long
    Dim r As Boolean
    Dim MfnFileName As Long
    Dim MfnOrder As Long
    Dim d As String
    
    If Len(record) > 0 Then
        q = getMfnByFilename(filename, Mfns)
        If q > 0 Then
            MfnFileName = Mfns(1)
        End If
        q = getMfnByOrder(order, Mfns)
        If q > 0 Then
            MfnOrder = Mfns(1)
        End If
        If MfnFileName = MfnOrder Then
            d = Date$
            d = Mid(d, 7, 4) & Mid(d, 1, 2) & Mid(d, 4, 2)
            
            record = record + isis.TagContents(d, 91)
            r = isis.Save(record, MfnFileName)
        End If
    End If
    
    ImportRecord = r
End Function


Function getRecordContent(filename As String) As String
    Dim q As Long
    Dim Mfns() As Long
    Dim tagged As String
    
    q = getMfnByFilename(filename, Mfns)
    If q > 0 Then
        tagged = isis.RecordGet(Mfns(1))
    End If
    getRecordContent = tagged
End Function
