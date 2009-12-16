VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClBodyElem"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public no As String

Public name As String

Public content As String

Public Children As ColBodyElem

Public parent As ClBodyElem

Public level As Long

Public Key As String

Public Tp As String

Const separador = ""

Public Function Path() As String
    
    Dim father As ClBodyElem
    Dim lfather As String
    
    Set father = parent
    
    While Not (father Is Nothing)
        lfather = lfather + separador + father.Key
        Set father = father.parent
    Wend
    Path = Key + separador + Trim(lfather)
End Function

Public Function listParents(tag As Long) As String
    Dim par As String
    Dim father As ClBodyElem
    Dim lfather As String
    
    Set father = parent
    
    While Not (father Is Nothing)
        If father.level >= 0 Then
            par = par + TagContents(Trim(father.Path) + "^n" + CStr(father.level), tag)
            
        End If
        Set father = father.parent
    Wend
    listParents = par
End Function

Public Function listChildren(tag As Long) As String
    Dim ch As String
    Dim child As ClBodyElem
    Dim i As Long
    
    For i = 1 To Children.Count
        Set child = Children(i)
        
        ch = ch + TagContents(Trim(child.Path) + "^n" + CStr(child.level), tag)
        
    Next
    listChildren = ch
End Function


