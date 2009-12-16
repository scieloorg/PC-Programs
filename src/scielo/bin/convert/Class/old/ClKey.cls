VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClKey"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private mvarindex As Long 'local copy

Public Property Let index(ByVal vData As Long)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Index = 5
    mvarindex = vData
End Property

Public Property Get index() As Long
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Index
    index = mvarindex
End Property

