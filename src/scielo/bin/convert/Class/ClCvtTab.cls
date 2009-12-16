VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClCvtTab"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private charlist As ColPair
Public key As String

Function ReadTable(Path As String, File As String, Separator As String) As Boolean
    Dim Line As String
    Dim elem As ClPair
    Dim elem1 As String
    Dim elem2 As String
    Dim fn As Long
    Dim c As ClPair
    Dim c1 As String
    Dim c2 As String
    Dim existbin As Boolean
    Dim existtxt As Boolean
    
    Set c = New ClPair
    Set elem = New ClPair
    
    fn = FreeFile
    Open Path + "\" + File For Input As fn
    Debug.Print File
    While Not EOF(fn)
        Line Input #fn, Line
        Debug.Print Line
        elem1 = Mid(Line, 1, InStr(Line, Separator) - 1)
        elem2 = Mid(Line, InStr(Line, Separator) + 1)
        
        c1 = Mid(elem1, 1, 1)
        If Len(elem1) > 1 Then
            c2 = Mid(elem1, Len(elem1), 1)
        Else
            c2 = ""
        End If
        
        Set c = charlist.Item(c1 + c2, existtxt)
        If Not existtxt Then
            Set c = charlist.Add(c1 + c2)
            c.elem1 = c1
            c.elem2 = c2
        End If
        
        Set elem = c.Pointer.AddBin(elem1, elem1)
        elem.elem1 = elem1
        elem.elem2 = elem2
    Wend
    Close fn
    
    ReadTable = (charlist.Count > 0)
End Function


Function Convert(r As String) As String
    Dim i As Long
    Dim j As Long
    Dim s As String
    Dim p1 As Long
    Dim found As Boolean
    
    
    s = r
    For i = 1 To charlist.Count
        With charlist(i)
        j = 0
        
        p1 = InStr(1, s, .elem1, vbTextCompare)
        If p1 > 0 Then
            If Len(.elem2) > 0 Then
                If InStr(p1 + 1, s, .elem2, vbTextCompare) > 0 Then
                    found = True
                End If
            Else
                found = True
            End If
        End If
        
        While (found) And (j < .Pointer.Count)
            j = j + 1
            s = ReplaceString(s, .Pointer(j).elem1, .Pointer(j).elem2, vbBinaryCompare)
            'Debug.Print "present=" & .Pointer(j).elem1 & "->" & .Pointer(j).elem2 & "."
            
            p1 = InStr(1, s, .elem1, vbTextCompare)
            If p1 > 0 Then
                If Len(.elem2) > 0 Then
                    If InStr(p1 + 1, s, .elem2, vbTextCompare) > 0 Then
                        found = True
                    End If
                Else
                    found = True
                End If
            End If
        Wend
        End With
    Next
    Convert = s
End Function

Private Sub Class_Initialize()
    Set charlist = New ColPair
End Sub

Private Sub Class_Terminate()
    Set charlist = Nothing
End Sub
