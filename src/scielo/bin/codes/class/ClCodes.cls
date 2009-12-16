VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClCodes"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Sub InsertElem(FilledList As ListBox, Code As String, value As String)
    Dim i As Long
    Dim found As Boolean
    
    If (Len(Code) > 0) And (Len(value) > 0) Then
        While (Not found) And (i < FilledList.ListCount)
            If InStr(1, FilledList.List(i), Code, vbBinaryCompare) = 1 Then
                found = True
            Else
                i = i + 1
            End If
        Wend
        If found Then
            FilledList.RemoveItem (i)
            FilledList.AddItem Code + "-" + value
        Else
            FilledList.AddItem Code + "-" + value
        End If
    End If
End Sub

Sub RemoveElem(FilledList As ListBox, Code As String, value As String)
    Dim i As Long
    Dim found As Boolean
    Dim res As VbMsgBoxResult
    
    If (Len(Code) > 0) And (Len(value) > 0) Then
        While (Not found) And (i < FilledList.ListCount)
            If StrComp(FilledList.List(i), Code + "-" + value, vbBinaryCompare) = 0 Then
                found = True
            Else
                i = i + 1
            End If
        Wend
        If found Then
            res = MsgBox("Are you sure you want to delete?", vbYesNo)
            If res = vbYes Then
                FilledList.RemoveItem (i)
            End If
        End If
    End If
End Sub

Sub SelectedCodeValue(ListFilled As ListBox, Code As String, Val As String)
    Dim p As Long
    Dim choice As String
    
    choice = ListFilled.List(ListFilled.ListIndex)
    p = InStr(choice, "-")
    Code = Mid(choice, 1, p - 1)
    Val = Mid(choice, p + 1)

End Sub

Function GetValue(FilledList As ListBox, Code As String) As String
    Dim i As Long
    Dim found As Boolean
    Dim value As String
    
    If (Len(Code) > 0) Then
        While (Not found) And (i < FilledList.ListCount)
            If InStr(1, FilledList.List(i), Code + "-", vbBinaryCompare) = 1 Then
                found = True
            Else
                i = i + 1
            End If
        Wend
        If found Then
            value = Mid(FilledList.List(i), InStr(FilledList.List(i), "-") + 1)
        End If
    End If
    GetValue = value
End Function

Sub OpenCodes(List As ListBox, Category As String, Optional Language As String)
    Dim isisCode As ClIsisDll
    Dim q As Long
    Dim Mfns() As Long
    Dim Item As String
    Dim res  As String
    Dim p As Long
    Dim found As Boolean
    Dim i As Long
    
    Set isisCode = New ClIsisDll
    If isisCode.Inicia(DBCODESPATH, DBNEWCODEFILE, DBCODESLABEL) Then
        If isisCode.IfCreate(DBNEWCODEFILE) Then
            q = isisCode.MfnFind(Language + "-" + Category, Mfns)
            While (Not found) And (i < q)
                i = i + 1
                If (StrComp(Category, isisCode.UsePft(Mfns(i), "v1^*")) = 0) And (StrComp(Language, isisCode.UsePft(Mfns(i), "v1^l")) = 0) Then
                    found = True
                End If
            Wend
            If found Then
                res = isisCode.UsePft(Mfns(i), "(v2^c|-|,v2^v/)")
                p = InStr(res, vbCrLf)
                While p > 0
                    Item = Mid(res, 1, p - 1)
                    If Len(Item) > 0 Then List.AddItem Item
                    res = Mid(res, p + 2)
                    p = InStr(res, vbCrLf)
                Wend
            End If
        End If
    End If
    Set isisCode = Nothing
End Sub
Sub SaveCodes(List As ListBox, Category As String, Optional Language As String)
    Dim isisCode As ClIsisDll
    Dim q As Long
    Dim Mfns() As Long
    Dim Mfn As Long
    Dim res  As String
    Dim p As Long
    Dim found As Boolean
    Dim i As Long
    Dim id As String
    
    Set isisCode = New ClIsisDll
    If isisCode.Inicia(DBCODESPATH, DBNEWCODEFILE, DBCODESLABEL) Then
        If isisCode.IfCreate(DBNEWCODEFILE) Then
            id = Language + "-" + Category
            q = isisCode.MfnFind(id, Mfns)
            While (Not found) And (i < q)
                i = i + 1
                If (StrComp(Category, isisCode.UsePft(Mfns(i), "v1^*")) = 0) And (StrComp(Language, isisCode.UsePft(Mfns(i), "v1^l")) = 0) Then
                    found = True
                    Mfn = Mfns(i)
                End If
            Wend
            If Len(Language) > 0 Then res = "^l" + Language
            res = TagContent(Category + res, 1)
            If found Then
                For i = 0 To List.ListCount - 1
                    p = InStr(List.List(i), "-")
                    res = res + TagContent("^c" + Mid(List.List(i), 1, p - 1) + "^v" + Mid(List.List(i), p + 1), 2)
                Next
                If isisCode.RecordUpdate(Mfn, res) Then
                    Call isisCode.IfUpdate(Mfn, Mfn)
                End If
            Else
                Mfn = isisCode.RecordSave(res)
                If Mfn > 0 Then Call isisCode.IfUpdate(Mfn, Mfn)
            End If
        End If
    End If
    Set isisCode = Nothing
End Sub

Private Function TagContent(ByVal Content As String, tag As Long) As String
    If (Len(Content) > 0) And (tag > 0) Then
        Content = "<" + CStr(tag) + ">" + Content + "</" + CStr(tag) + ">" + vbCrLf
    End If
    TagContent = Content
End Function
Function Codes_ChangedContents(List As ListBox, Category As String, Optional Language As String) As Boolean
    Dim isisCode As ClIsisDll
    Dim q As Long
    Dim Mfns() As Long
    Dim Mfn As Long
    Dim db  As String
    Dim Form As String
    Dim p As Long
    Dim found As Boolean
    Dim i As Long
    Dim change As Boolean
    
    Set isisCode = New ClIsisDll
    If isisCode.Inicia(DBCODESPATH, DBNEWCODEFILE, DBCODESLABEL) Then
        If isisCode.IfCreate(DBNEWCODEFILE) Then
            q = isisCode.MfnFind(Language + "-" + Category, Mfns)
            While (Not found) And (i < q)
                i = i + 1
                If (StrComp(Category, isisCode.UsePft(Mfns(i), "v1^*")) = 0) And (StrComp(Language, isisCode.UsePft(Mfns(i), "v1^l")) = 0) Then
                    found = True
                    Mfn = Mfns(i)
                    db = isisCode.UsePft(Mfn, "(v2^c|-|,v2^v/)")
                End If
            Wend
            For i = 0 To List.ListCount - 1
                Form = Form + List.List(i) + vbCrLf
            Next
            change = (StrComp(Form, db, vbBinaryCompare) <> 0)
        End If
    End If
    Set isisCode = Nothing
    Codes_ChangedContents = change
End Function

Function GenerateFile(DBCODEFILE As String, Category As String, Optional Language As String) As String
    Dim isisCode As ClIsisDll
    Dim q As Long
    Dim Mfns() As Long
    Dim Item As String
    Dim res  As String
    Dim p As Long
    Dim found As Boolean
    Dim i As Long
    
    Set isisCode = New ClIsisDll
    If isisCode.Inicia(DBCODESPATH, DBCODEFILE, DBCODESLABEL) Then
        If isisCode.IfCreate(DBCODEFILE) Then
            q = isisCode.MfnFind(Language + "-" + Category, Mfns)
            While (Not found) And (i < q)
                i = i + 1
                If (StrComp(Category, isisCode.UsePft(Mfns(i), "v1^*")) = 0) And (StrComp(Language, isisCode.UsePft(Mfns(i), "v1^l")) = 0) Then
                    found = True
                End If
            Wend
            res = Category + vbCrLf
            If found Then
                res = res + isisCode.UsePft(Mfns(i), "(v2^v+|;|)") + vbCrLf
                res = res + isisCode.UsePft(Mfns(i), "(v2^c+|;|)") + vbCrLf
            Else
                res = res + vbCrLf
                res = res + vbCrLf
            End If
        End If
    End If
    Set isisCode = Nothing
    GenerateFile = res
End Function

