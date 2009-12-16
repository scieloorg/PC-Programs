VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClIdiom"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable(s) to hold property value(s)
Private mvarCode As String 'local copy
Private mvarLabel As String 'local copy
Private mvarMore As String 'local copy
Private mvarindex As Long 'local copy

Public Property Let index(ByVal vData As Long)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.index = 5
    mvarindex = vData
End Property

Public Property Get index() As Long
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.index
    index = mvarindex
End Property

Public Property Let More(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.More = 5
    mvarMore = vData
End Property

Public Property Set More(ByVal vData As Variant)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.More = Form1
    mvarMore = vData
End Property

Public Property Get More() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.More
        More = mvarMore
End Property

Public Property Let label(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Label = 5
    mvarLabel = vData
End Property

Public Property Get label() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Label
    label = mvarLabel
End Property

Public Property Let Code(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Code = 5
    mvarCode = vData
End Property

Public Property Get Code() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Code
    Code = mvarCode
End Property

