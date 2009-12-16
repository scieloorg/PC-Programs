VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClLink"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public Id As Variant 'local copy
Public Field As Long 'local copy
Public Ref As String 'local copy

Private mvarRIdCount As Long 'local copy
Private mvarRId() As Variant 'local copy

Public Property Let RIdCount(ByVal vData As Long)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.RIdCount = 5
    ReDim Preserve mvarRId(vData)
    mvarRIdCount = vData
End Property


Public Property Get RIdCount() As Long
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.RIdCount
    RIdCount = mvarRIdCount
End Property

Public Property Let RId(i As Long, ByVal vData As Variant)
    If i > RIdCount Then RIdCount = i
    mvarRId(i) = vData
End Property

Public Property Set RId(i As Long, ByVal vData As Object)
    If i > RIdCount Then RIdCount = i
    Set mvarRId(i) = vData
End Property

Public Property Get RId(i As Long) As Variant
    If i <= RIdCount Then
        RId = mvarRId(i)
    Else
        
    End If
End Property

Private Sub Class_Terminate()
    Erase mvarRId
End Sub
