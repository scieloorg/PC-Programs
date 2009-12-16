VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClCode"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
'local variable(s) to hold property value(s)
Private mvarCode As String 'local copy
Private mvarValue As String 'local copy
Public index As Long

Public unabled As Boolean

Public Property Let value(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Value = 5
    mvarValue = vData
End Property


Public Property Get value() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Value
    value = mvarValue
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



