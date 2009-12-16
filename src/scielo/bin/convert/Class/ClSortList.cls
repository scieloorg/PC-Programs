VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClSortList"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private Elements() As String
Private Count As Long

Private Property Let counter(v As Long)
    Count = v
    ReDim Preserve Elements(v)
End Property

Property Get counter() As Long
    counter = Count
End Property

Public Function exist(elem As String) As Boolean
    Dim j As Long
    Dim found As Boolean
    Dim i As Long
    Dim k As Long
    
    While (i < counter) And (j = 0)
        i = i + 1
        k = StrComp(elem, Elements(i), vbBinaryCompare)
        If k = 0 Then
            j = i
        ElseIf k < 0 Then
            i = counter
        End If
    Wend
    
    
    exist = (j > 0)
End Function

Public Function RemoveElem(elem As String) As Boolean
    Dim j As Long
    Dim found As Boolean
    Dim i As Long
    Dim k As Long
    
    
        While (i < counter) And (j = 0)
            i = i + 1
            k = StrComp(elem, Elements(i), vbBinaryCompare)
            If k > 0 Then
                i = counter
            ElseIf k = 0 Then
                j = i
            End If
        Wend
    
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

Public Function Insert(elem As String) As Boolean
    Dim i As Long
    Dim j As Long
    Dim k As Long
    
    While (i < counter) And (j = 0)
        i = i + 1
        k = StrComp(elem, Elements(i), vbBinaryCompare)
        If k < 0 Then
            j = i
        End If
    Wend
    If j > 0 Then
        
        counter = counter + 1
        
        i = counter
        While (i > j)
            Elements(i) = Elements(i - 1)
            i = i - 1
        Wend
        Elements(j) = elem
        Insert = True
    Else
        counter = counter + 1
        Elements(counter) = elem
        Insert = True
    End If
    
End Function


Public Function GetElem(i As Long) As String
    Dim e As String
    
    If i <= counter Then
        e = Elements(i)
    End If
    GetElem = e
End Function

Private Sub Class_Terminate()
    Erase Elements
End Sub
