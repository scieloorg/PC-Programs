VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClLista"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private Elements() As Variant
Private Count As Long

Private Property Let counter(v As Long)
    Count = v
    ReDim Preserve Elements(v)
End Property

Private Property Get counter() As Long
    counter = Count
End Property

Function ElemStr(i As Long) As String
    If (i <= counter) And (i > 0) Then ElemStr = Elements(i)
End Function

Function ElemLng(i As Long) As Long
    If (i <= counter) And (i > 0) Then ElemLng = Elements(i)
End Function

Public Function existe(elem As Variant) As Boolean
    Dim j As Long
    Dim found As Boolean
    Dim i As Long
    
    While (i < counter) And (j = 0)
        i = i + 1
        If StrComp(elem, Elements(i), vbTextCompare) = 0 Then
            j = i
        End If
    Wend
       existe = (j > 0)
End Function

Public Function RemoveElem(elem As Variant, Optional Index As Long) As Boolean
    Dim j As Long
    Dim found As Boolean
    Dim i As Long
    
    If Index > 0 Then
        If StrComp(elem, Elements(Index), vbTextCompare) = 0 Then
            j = Index
        End If
    Else
        While (i < counter) And (j = 0)
            i = i + 1
            If StrComp(elem, Elements(i), vbTextCompare) = 0 Then
                j = i
            End If
        Wend
    End If
    
    If j > 0 Then
        found = True
        i = j
        While (i < counter)
            i = i + 1
            If i > 1 Then
                Elements(i - 1) = Elements(i)
            End If
        Wend
        counter = counter - 1
    End If
    
    RemoveElem = found
End Function

Public Function RemoveFirst(elem As Variant) As Boolean
    If counter > 0 Then
        elem = Elements(1)
        RemoveFirst = RemoveElem(elem, 1)
    End If
    
End Function

Public Function RemoveLast(elem As Variant) As Boolean
    If counter > 0 Then
        elem = Elements(counter)
        RemoveLast = RemoveElem(elem, counter)
    End If
    
End Function

Public Function Insere(elem As Variant) As Boolean
    counter = counter + 1
    Elements(counter) = elem
    Insere = True
End Function

Private Sub Class_Terminate()
    Erase Elements
End Sub
