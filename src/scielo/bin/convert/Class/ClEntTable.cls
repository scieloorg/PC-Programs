VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClEntTable"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private first As Long
Private last As Long

Private field1() As String
Private field2() As String

Private vField1() As String
Private vField2() As String
Private PrevField() As Long
Private NextField() As Long
Private Count As Long

Private Property Let Counter(v As Long)
    Count = v
    ReDim Preserve vField1(v)
    ReDim Preserve vField2(v)
    ReDim Preserve PrevField(v)
    ReDim Preserve NextField(v)
End Property

Property Get Counter() As Long
    Counter = Count
End Property

Public Function exist(elem1 As String, elem2 As String) As Boolean
    Dim j As Long
    Dim found As Boolean
    Dim i As Long
    Dim k As Long
    
    i = 1
    While (i < Counter) And (j = 0)
        i = i + 1
        k = StrComp(elem1, field1(i), vbBinaryCompare)
        If k = 0 Then
            j = i
            elem2 = field2(i)
        ElseIf k < 0 Then
            i = Counter
        End If
    Wend
    
    
    exist = (j > 0)
End Function

Public Function Insert(elem1 As String, elem2 As String) As Boolean
    Dim i As Long
    Dim j As Long
    Dim k As Long
    Dim prev As Long
    Dim curr As Long
    Debug.Print Counter, elem1
    curr = first
    While (j = 0) And (curr > 0)
            k = StrComp(elem1, vField1(curr), vbBinaryCompare)
            If k < 0 Then
                j = curr
            End If
            prev = curr
            curr = NextField(curr)
    Wend
    
    If j > 0 Then
        'element between or first
        Counter = Counter + 1
        vField1(Counter) = elem1
        vField2(Counter) = elem2
        PrevField(Counter) = PrevField(j)
        NextField(Counter) = j
        If PrevField(j) > 0 Then NextField(PrevField(j)) = Counter
        PrevField(j) = Counter
        If vField1(Counter) < vField1(first) Then first = Counter
        
        Insert = True
    Else
        'last element or the only one
        Counter = Counter + 1
        vField1(Counter) = elem1
        vField2(Counter) = elem2
        PrevField(Counter) = prev
        NextField(Counter) = 0
        last = Counter
        If prev > 0 Then NextField(prev) = Counter
        If first = 0 Then first = 1
        
        Insert = True
    End If
    
End Function


Public Function SortInsert() As Boolean
    Dim i As Long
    Dim curr As Long
    
    ReDim field1(Counter)
    ReDim field2(Counter)
        
    curr = first
    
    While curr > 0
        i = i + 1
        field1(i) = vField1(curr)
        field2(i) = vField2(curr)
        Debug.Print i, field1(i), field2(i)
        curr = NextField(curr)
    Wend
        
End Function

Function ReadTable(Path As String, File As String) As Boolean
    Dim Line As String
    Dim f1 As String
    Dim f2 As String
    Dim fn As Long
    
       fn = 1
        Open Path + "\" + File For Input As fn
        While Not EOF(fn)
            Line Input #fn, Line
            f1 = Mid(Line, 1, InStr(Line, Chr(9)) - 1)
            f2 = Mid(Line, InStr(Line, Chr(9)) + 1)
            Call Insert(f1, f2)
            Debug.Print f1, f2
        Wend
        Close fn
        SortInsert
    
    ReadTable = (Counter > 0)
End Function


