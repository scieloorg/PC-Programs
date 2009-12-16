VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClHTML"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit



Function loadHTML(sHTML As String) As ClHTMLNode
    Dim textBefore As String, textMiddle As String, textAfter As String, tagInitial As String, tagEnd As String
    Dim root As New ClHTMLNode
    
    Set root.Middle = New ClHTMLNodes
    root.FormerText = sHTML
    Do
        Call extract(sHTML, textBefore, textMiddle, textAfter, tagInitial, tagEnd)
        Call createNode(root.Middle, textBefore, textMiddle, tagInitial, tagEnd)
        sHTML = textAfter
    Loop While Len(textAfter) > 0
    Set loadHTML = root
End Function

Sub extract(sHTML As String, textBefore As String, textMiddle As String, textAfter As String, tagInitial As String, tagEnd As String)
    Dim p As Long
    Dim p2 As Long
    Dim pEnd As Long
    Dim Tag As String
    
    textMiddle = ""
    tagInitial = ""
    tagEnd = ""
    
    p = InStr(sHTML, "<")
    If p > 0 Then
        textBefore = Mid(sHTML, 1, p - 1)
    
        sHTML = Mid(sHTML, p)
        pEnd = InStr(sHTML, ">")
        tagInitial = Mid(sHTML, p, pEnd)
        
        sHTML = Mid(sHTML, pEnd + 1)
        tagEnd = "</" + Tag + ">"
    
        p2 = InStr(sHTML, tagEnd)
    
        textMiddle = Mid(sHTML, 1, p2 - 1)
        textAfter = Mid(sHTML, p2 + Len(tagEnd))
    Else
        textBefore = sHTML
        textAfter = ""
    End If
           
End Sub

Sub createNode(nodes As ClHTMLNodes, textBefore As String, textMiddle As String, tagInitial As String, tagEnd As String)
    Dim node As ClHTMLNode
    Dim node2 As ClHTMLNode
    
    If Len(textBefore) > 0 Then
        Set node = New ClHTMLNode
        node.Text = textBefore
        node.CleanedText = cleanText(textBefore)
        nodes.Add (node)
    End If
    If Len(textMiddle) > 0 Then
        Set node2 = loadHTML(textMiddle)
        node2.tagInitial = tagInitial
        node2.tagEnd = tagEnd
        
        nodes.Add (node2)
    End If
End Sub
