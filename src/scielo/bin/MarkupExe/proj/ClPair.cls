VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClFileInfo"
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
Public Pointer As ColFileInfo
'local variable(s) to hold property value(s)
Private mvarelem3 As String 'local copy
Private mvarelem4 As Boolean

Public Property Let required(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.required = 5
    mvarelem4 = vData
End Property


Public Property Get required() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.required
    required = mvarelem4
End Property




Public Property Let filename(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.filename = 5
    mvarelem3 = vData
End Property


Public Property Get filename() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.filename
    filename = mvarelem3
End Property






Public Property Let path(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.path = 5
    mvarelem2 = vData
End Property


Public Property Get path() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.path
    path = mvarelem2
End Property



Public Property Let key(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.key = 5
    mvarelem1 = vData
End Property


Public Property Get key() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.key
    key = mvarelem1
End Property



Private Sub Class_Initialize()
    Set Pointer = New ColFileInfo
End Sub

Private Sub Class_Terminate()
    Set Pointer = Nothing
End Sub
