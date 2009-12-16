VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClHTMLNodes"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private nodes As New Collection

Function Add(Item As ClHTMLNode) As ClHTMLNode
    Call nodes.Add(Item, CStr(nodes.Count + 1))
End Function
Function Item(i As Long) As ClHTMLNode
    Set Item = nodes(i)
End Function
Function Count() As Long
    Count = nodes.Count
End Function

Function getText() As String
    Dim r As String
    Dim i As Long
    
    For i = 1 To nodes.Count
        r = r & nodes.Item(i).getText()
    Next
    getText = r
End Function
Function getCleanedText() As String
    Dim r As String
    Dim i As Long
    
    For i = 1 To nodes.Count
        r = r & nodes.Item(i).getCleanedText()
    Next
    getCleanedText = r
End Function

