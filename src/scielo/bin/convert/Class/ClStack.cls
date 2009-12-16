VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClStack"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable(s) to hold property value(s)
Private stack() As String
Private count As Long

Public Sub Insert(elem As String)
    count = count + 1
    ReDim Preserve stack(count)
    stack(count) = elem
End Sub

Public Function Remove(elem As String) As Boolean
    Dim ret As Boolean
    
    If count > 0 Then
        elem = stack(count)
        count = count - 1
        ReDim Preserve stack(count)
        ret = True
    End If
    Remove = ret
End Function

Public Property Get Top() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Top
    Top = stack(count)
End Property



Private Sub Class_Initialize()
    
End Sub

Private Sub Class_Terminate()
    Erase stack
    count = 0
End Sub
