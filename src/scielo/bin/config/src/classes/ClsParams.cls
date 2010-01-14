VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsParams"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private col As New Collection

Sub add(value As Variant, key As Variant)
    Call col.add(value, key)
        'Call col.add(value, key)
End Sub
Function count() As Long
    count = col.count
End Function

Property Get item(index As Variant) As Variant
On Error Resume Next
  item = col.item(index)
End Property
Property Let item(index As Variant, v As Variant)
On Error Resume Next
  col.item(index) = v
End Property

