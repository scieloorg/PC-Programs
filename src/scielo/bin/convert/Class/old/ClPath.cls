VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClPath"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable(s) to hold property value(s)
Private mvarDirName As String 'local copy
Private mvarFileName As String 'local copy
Private mvarlabel As String 'local copy
Private mvarPType As String 'local copy
Private mvarKey As String 'local copy

Public Property Let Key(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Key = 5
    mvarKey = vData
End Property

Public Property Get Key() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Key
    Key = mvarKey
End Property

Public Property Let PType(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.PType = 5
    mvarPType = vData
End Property

Public Property Get PType() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.PType
    PType = mvarPType
End Property

Public Property Let label(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Label = 5
    mvarlabel = vData
End Property

Public Property Get label() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Label
    label = mvarlabel
End Property

Public Property Let FileName(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.text = 5
    mvarFileName = vData
End Property

Public Property Get FileName() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.text
    FileName = mvarFileName
End Property

Public Property Let DirName(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.parent.fullpath = 5
    mvarDirName = vData
End Property

Public Property Get DirName() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.parent.fullpath
    DirName = mvarDirName
End Property

