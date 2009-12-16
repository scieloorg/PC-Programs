VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClListaOrd"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private Elements() As Variant
Private Counter As Long


Function ElemStr(i As Long) As String
    If (i <= Counter) And (i > 0) Then ElemStr = Elements(i)
End Function

Function ElemLng(i As Long) As Long
    If (i <= Counter) And (i > 0) Then ElemLng = Elements(i)
End Function

Public Function existe(Elem As Variant) As Boolean
    Dim j As Long
    Dim found As Boolean
    
    While (i < Counter) And (j = 0)
        i = i + 1
        If StrComp(Elem, Elements(i), vbBinaryCompare) >= 0 Then
            j = i
        End If
    Wend
    
    If j > 0 Then
        If StrComp(Elem, Elements(j), vbBinaryCompare) = 0 Then
            found = True
        End If
    End If
    existe = found
End Function

Public Function Remove1(Elem As Variant) As Boolean
    Dim j As Long
    Dim found As Boolean
    
    While (i < Counter) And (j = 0)
        i = i + 1
        If StrComp(Elem, Elements(i), vbBinaryCompare) >= 0 Then
            j = i
        End If
    Wend
    
    If j > 0 Then
        If StrComp(Elem, Elements(j), vbBinaryCompare) = 0 Then
            found = True
            i = j
            While (i < Counter)
                i = i + 1
                Elements(i - 1) = Elements(i)
            Wend
        End If
    End If
    Remove1 = found
End Function

Public Function Remove2(Elem As Variant) As Boolean
    Elem = Elements(1)
    Remove2 = Remove1(Elem)
End Function

Public Function Insere(Elem As Variant) As Boolean
    Dim j As Long
    
    While (i < Counter) And (j = 0)
        i = i + 1
        If StrComp(Elem, Elements(i), vbBinaryCompare) >= 0 Then
            j = i
        End If
    Wend
    Counter = Counter + 1
    
    If j = 0 Then
        j = Counter
        ReDim Preserve Elements(Counter)
        Elements(Counter) = Elem
    Else
        i = Counter
        While (i > j)
            i = i - 1
            Elements(i + 1) = Elements(i)
        Wend
    End If
    Insere = (j > 0)
End Function

