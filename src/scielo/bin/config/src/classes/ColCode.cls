VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColCode"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"ClCode"
Attribute VB_Ext_KEY = "Member0" ,"ClCode"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit


Private mCol As Collection
Public lang As String

Public Function add(obj As ClCode, SKEY As String) As ClCode
    
    Call mCol.add(obj, SKEY)
    Set add = obj


End Function

Public Property Get item(vntIndexKey As Variant, Optional exist As Boolean) As ClCode
Attribute item.VB_UserMemId = 0
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
    
    Dim i As Long
    
    On Error GoTo NOT_FOUND
    exist = True
    Set item = mCol.item(vntIndexKey)
    
    
    
    
    Exit Property
    
NOT_FOUND:
exist = False
While (Not exist) And (i < count)
        i = i + 1
        If StrComp(vntIndexKey, mCol(i).value, vbTextCompare) = 0 Or StrComp(vntIndexKey, mCol(i).Code) = 0 Then
            exist = True
            Set item = mCol(i)
        End If
    Wend
End Property



Public Property Get count() As Long
    'used when retrieving the number of elements in the
    'collection. Syntax: Debug.Print x.Count
    count = mCol.count
End Property


Public Sub remove(vntIndexKey As Variant)
    'used when removing an element from the collection
    'vntIndexKey contains either the Index or Key, which is why
    'it is declared as a Variant
    'Syntax: x.Remove(xyz)


    mCol.remove vntIndexKey
End Sub


Private Sub Class_Initialize()
    'creates the collection when this class is created
    Set mCol = New Collection
End Sub


Private Sub Class_Terminate()
    'destroys collection when this class is terminated
    Set mCol = Nothing
End Sub

