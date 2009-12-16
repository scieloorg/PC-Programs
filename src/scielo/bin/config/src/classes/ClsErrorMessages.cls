VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsErrorMessages"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private errors As New Collection

Sub add(message As String, key As String)
    Call errors.add(message, key)
End Sub

Function count() As Long
    count = errors.count
End Function

Function item(index As Variant) As String
On Error Resume Next
    item = errors.item(index)
End Function

Sub display(key As String, Optional params As ClsParams)
    MsgBox getMessage(key, params)
End Sub
Function getMessage(key As String, Optional params As ClsParams) As String
    Dim s As String
    Dim i As Long
    
    s = errors.item(key)
    If Len(s) = 0 Then
        s = key
    End If
    
    
    If Not params Is Nothing Then
    For i = 1 To params.count
        s = Replace(s, "%PARAM" + CStr(i) + "%", params.item(i))
    Next
    End If
    getMessage = s
End Function

Sub load(FileName As String)
    Dim fn As Long
    Dim m As String
    Dim key As String
    Dim message As String
    
    fn = FreeFile
    If "langs\" + Dir(FileName) = FileName Then
        Open FileName For Input As fn
        While Not EOF(fn)
            Input #fn, key, message
            m = message
            Call add(m, key)
        Wend
        Close #fn
    Else
        MsgBox "no error messages"
    End If
End Sub
