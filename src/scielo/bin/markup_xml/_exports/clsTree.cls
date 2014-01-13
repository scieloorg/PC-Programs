VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsTree"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private tree As Collection



Sub load()
    Dim f As Long
    Dim line As String
    Dim splited() As String
    Dim node As clsNode
    Dim child As clsChild
    
    Set tree = New Collection
    
    f = FreeFile
    Open MyMacro.markupprg_path & "\app_core\tree.txt" For Input As #f
    While Not EOF(f)
        ok = True
        Input #f, line
        If Len(line) > 0 Then
            If InStr(line, ";") > 0 Then
                Set child = New clsChild
                splited = Split(line, ";")
                child.name = splited(0)
                child.is_repetitive = (splited(1) = "#TRUE#")
                node.add_child (child)
            Else
                Set node = New clsNode
                node.name = line
            End If
        Else
            Call tree.add(node, node.name)
        End If
    Wend
    Close #f
End Sub

Function get_node(name As String) As clsNode
    Set get_node = tree.item(name)
End Function
