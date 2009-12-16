VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClDocOrder"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Function getOrderFormats(documentOrder As String, ByRef Count As Long) As Variant
    Dim i As Long
    Dim numberOfDigits As Long
    Dim formatedOrder() As String
    Count = 0
    For i = 0 To UBound(BV(Currbv).getDocOrderLen(-1))
        numberOfDigits = CLng(BV(Currbv).getDocOrderLen(i))
        If Len(documentOrder) > numberOfDigits Then
            'nao seria possivel encontrar na base
        Else
            ' formata o order para que ele seja encontrado na base,
            ' de acordo com a quantidade de dígitos exigida pelos padrões disponíveis
            Count = Count + 1
            ReDim Preserve formatedOrder(Count)
            formatedOrder(Count) = Replace(Space(numberOfDigits - Len(documentOrder)), " ", "0") + documentOrder
        End If
    Next
    getOrderFormats = formatedOrder
End Function
    
Function formatOrder(documentOrder As String) As String
    Dim i As Long
    Dim numberOfDigits As Long
    Dim formatedOrder As String
    
    i = 0
    formatedOrder = ""
    While i < UBound(BV(Currbv).getDocOrderLen(-1)) And (formatedOrder = "")
        
        numberOfDigits = CLng(BV(Currbv).getDocOrderLen(i))
        If Len(documentOrder) > numberOfDigits Then
            'nao seria possivel encontrar na base
        Else
            ' formata o order para que ele seja encontrado na base,
            ' de acordo com a quantidade de dígitos exigida pelos padrões disponíveis
            formatedOrder = Replace(Space(numberOfDigits - Len(documentOrder)), " ", "0") + documentOrder
        End If
        i = i + 1
    Wend
    formatOrder = formatedOrder
End Function
    
