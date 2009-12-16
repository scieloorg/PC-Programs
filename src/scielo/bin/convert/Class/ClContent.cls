VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClContent"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Function TagContent(ByVal content As String, ByVal Tag As Long) As String
    Dim tagged As String
    Dim c As String
    
    c = content
    If Tag > 0 Then
        If Len(content) > 0 Then
            'content = changeDamagingContent(content)
            content = fixDamagingContent(1, content)
            If content <> c Then
                Debug.Print c
                Debug.Print content
            End If
            tagged = CONST_DELIM1 + CStr(Tag) + CONST_DELIM2 + content + CONST_DELIM1 + "/" + CStr(Tag) + CONST_DELIM2 + vbCrLf
        End If
    Else
        'msgbox "TagContents: tag=0. Conteudo=" + content
    End If
    TagContent = tagged
End Function


Function fixDamagingContent(start As Long, content As String) As String
    Dim text As String
    Dim p As Long
    
    p = findTextBetweenltAndgt(start, content, text)
    If p > 0 And p < Len(content) Then
        If validText(p, content, text) Then
            p = p + 1
        Else
            content = fixText(p, content, text)
        End If
        content = fixDamagingContent(p, content)
    End If
    fixDamagingContent = content
End Function
Function findTextBetweenltAndgt(start As Long, content As String, text As String) As Long
    Dim p As Long
    Dim p2 As Long
    
    p = InStr(start, content, "<", vbTextCompare)
    If p > 0 Then
        p2 = InStr(p, content, ">", vbTextCompare)
        If p2 > 0 Then
            text = Mid(content, p + 1, p2 - p - 1)
        End If
    End If
    findTextBetweenltAndgt = p
End Function
Function validText(p As Long, content As String, text As String) As Boolean
    Dim r As Boolean
    Dim s As String
    
    If Len(text) > 0 Then
        If (text Like Replace(Space(Len(text)), " ", "#")) Then
        
            s = "</" + text + ">"
            If InStr(p, content, s, vbTextCompare) > 0 Then
                r = True
            Else
                r = False
            End If
        ElseIf (text Like ("/" & Replace(Space(Len(text) - 1), " ", "#"))) Then
            
            s = "<" & Mid(text, 2) & ">"
            If InStr(1, Mid(content, 1, p), s, vbTextCompare) > 0 Then
                r = True
            Else
                r = False
            End If
        Else
            r = True
        End If
    Else
        r = True
    End If
    validText = r
End Function
Function fixText(p As Long, content As String, text As String) As String
    Dim r As String
    
    r = Mid(content, 1, p - 1) + "&lt;" + Mid(content, p + 1)
    fixText = r
End Function
