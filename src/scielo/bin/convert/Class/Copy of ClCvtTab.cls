VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClCvtTab"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private FirstChar As ClSortList
Private FChar As Collection

Private SortedKeys As ClSortList
Private Elements As ColPair

Property Get Counter() As Long
    Counter = Elements.Count
End Property

Public Function exist(elem1 As String, elem2 As String) As Boolean
    Dim found As Boolean
    
    Call Elements(elem1, found)
    If found Then
        elem2 = Elements(elem1).elem2
    End If
    exist = found
End Function

Private Sub BuildTree(elem1 As String, elem2 As String)
    Dim e As ClPair
    Dim exist As Boolean
    
    Set e = New ClPair
    Set e = Elements.Item(elem1, exist)
    If Not exist Then
        Set e = Elements.Add(elem1)
        e.elem1 = elem1
        e.elem2 = elem2
        
        SortedKeys.Insert (elem1)
    End If
    
End Sub

Function ReadTable(Path As String, file As String, Separator As String) As Boolean
    Dim Line As String
    Dim f1 As String
    Dim f2 As String
    Dim fn As Long
    
       fn = 1
        Open Path + "\" + file For Input As fn
        While Not EOF(fn)
            Line Input #fn, Line
            f1 = Mid(Line, 1, InStr(Line, Separator) - 1)
            f2 = Mid(Line, InStr(Line, Separator) + 1)
            Call BuildTree(f1, f2)
            Debug.Print f1, f2
        Wend
        Close fn
        SortInsert
    
    ReadTable = (Counter > 0)
End Function

Function Convert(s As String) As String
    Dim i As Long
    
    For i = 1 To Count
        s = ReplaceString(s, Elements(i).elem1, Elements(i).elem2, vbTextCompare)
    Next
    
    Convert = s
End Function
