VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClPair"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable(s) to hold property value(s)
Private mvarelem1 As String 'local copy
Private mvarelem2 As String 'local copy
Public Pointer As ColPair
'local variable(s) to hold property value(s)
Private mvarelem3 As String 'local copy
Private mvarelem4 As Boolean

Public Property Let elem4(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.elem4 = 5
    mvarelem4 = vData
End Property


Public Property Get elem4() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.elem4
    elem4 = mvarelem4
End Property




Public Property Let elem3(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.elem3 = 5
    mvarelem3 = vData
End Property


Public Property Get elem3() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.elem3
    elem3 = mvarelem3
End Property






Public Property Let elem2(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.elem2 = 5
    mvarelem2 = vData
End Property


Public Property Get elem2() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.elem2
    elem2 = mvarelem2
End Property



Public Property Let elem1(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.elem1 = 5
    mvarelem1 = vData
End Property


Public Property Get elem1() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.elem1
    elem1 = mvarelem1
End Property



Private Sub Class_Initialize()
    Set Pointer = New ColPair
End Sub

Private Sub Class_Terminate()
    Set Pointer = Nothing
End Sub
