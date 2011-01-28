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

Private privOrderLengthArray As Variant

Property Let OrderLengthArray(v As Variant)
    privOrderLengthArray = v
End Property
Property Get OrderLengthArray() As Variant
    OrderLengthArray = privOrderLengthArray
End Property

Function getFormattedOrders(documentOrder As String, ByRef Count As Long) As Variant
    Dim i As Long
    Dim numberOfDigits As Long
    Dim formatedOrder() As String
    
    Dim val As String
    Dim formatted As String
    
    
    val = CStr(CLng(documentOrder))
    Count = Count + 1
    ReDim Preserve formatedOrder(Count)
    formatedOrder(Count) = val
    
    For i = 0 To UBound(OrderLengthArray)
        numberOfDigits = CLng(OrderLengthArray(i))
        formatted = privFormatOrder(documentOrder, numberOfDigits)
        If val <> formatted Then
            Count = Count + 1
            ReDim Preserve formatedOrder(Count)
            formatedOrder(Count) = formatted
        End If
    Next
    getFormattedOrders = formatedOrder
End Function
    
Private Function privFormatOrder(documentOrder As String, numberOfDigits As Long) As String
    Dim formatedOrder As String
    
    If Len(documentOrder) <= numberOfDigits Then
        formatedOrder = Replace(Space(numberOfDigits - Len(documentOrder)), " ", "0") + documentOrder
    End If
    
    privFormatOrder = formatedOrder
End Function
    

Function formatOrder(documentOrder As String) As String
    Dim i As Long
    Dim numberOfDigits As Long
    Dim formatted As String
    
    i = 0
    
    While (Len(formatted) = 0) And (i <= UBound(OrderLengthArray))
        numberOfDigits = CLng(OrderLengthArray(i))
        formatted = privFormatOrder(documentOrder, numberOfDigits)
        i = i + 1
    Wend
    formatOrder = formatted
End Function
