VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsIssues"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private mCol As Collection

Public Sub add(objNewMember, Optional SKEY As String)

    If Len(SKEY) = 0 Then
        mCol.add objNewMember
    Else
        mCol.add objNewMember, SKEY
    End If
End Sub

Public Property Get item(vntIndexKey As Variant, Optional exist As Boolean) As Variant
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
    On Error GoTo NoExist
    
    If IsObject(mCol(vntIndexKey)) Then
        Set item = mCol(vntIndexKey)
        exist = True
    Else
        item = mCol(vntIndexKey)
        exist = True
    End If
    
    Exit Property
NoExist:
    exist = False
End Property



Public Property Get count() As Long
    'used when retrieving the number of elements in the
    'collection. Syntax: Debug.Print x.Count
    count = mCol.count
End Property


Public Function remove(vntIndexKey As Variant) As Boolean
    'used when removing an element from the collection
    'vntIndexKey contains either the Index or Key, which is why
    'it is declared as a Variant
    'Syntax: x.Remove(xyz)
    Dim existe As Boolean
    
    IsObject (item(vntIndexKey, existe))
    If existe Then mCol.remove vntIndexKey
    remove = existe
End Function


Private Sub Class_Initialize()
    'creates the collection when this class is created
    Set mCol = New Collection
End Sub


Private Sub Class_Terminate()
    'destroys collection when this class is terminated
    Set mCol = Nothing
End Sub


