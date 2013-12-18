VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsNode"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Public name As String
Public definition As String
Public children As Collection


Sub add_child(ch As clsChild)
    Call children.add(ch, ch.name)
End Sub

Function get_child(name As String) As clsChild
    Set get_child = children.item(name)
End Function
