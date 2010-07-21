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
    Dim P As Long
    
    P = findTextBetweenltAndgt(start, content, text)
    If P > 0 And P < Len(content) Then
        If validText(P, content, text) Then
            P = P + 1
        Else
            content = fixText(P, content, text)
        End If
        content = fixDamagingContent(P, content)
    End If
    fixDamagingContent = content
End Function
Function findTextBetweenltAndgt(start As Long, content As String, text As String) As Long
    Dim P As Long
    Dim p2 As Long
    
    P = InStr(start, content, "<", vbTextCompare)
    If P > 0 Then
        p2 = InStr(P, content, ">", vbTextCompare)
        If p2 > 0 Then
            text = Mid(content, P + 1, p2 - P - 1)
        End If
    End If
    findTextBetweenltAndgt = P
End Function
Function validText(P As Long, content As String, text As String) As Boolean
    Dim r As Boolean
    Dim s As String
    
    If Len(text) > 0 Then
        If (text Like Replace(Space(Len(text)), " ", "#")) Then
        
            s = "</" + text + ">"
            If InStr(P, content, s, vbTextCompare) > 0 Then
                r = True
            Else
                r = False
            End If
        ElseIf (text Like ("/" & Replace(Space(Len(text) - 1), " ", "#"))) Then
            
            s = "<" & Mid(text, 2) & ">"
            If InStr(1, Mid(content, 1, P), s, vbTextCompare) > 0 Then
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
Function fixText(P As Long, content As String, text As String) As String
    Dim r As String
    
    r = Mid(content, 1, P - 1) + "&lt;" + Mid(content, P + 1)
    fixText = r
End Function
