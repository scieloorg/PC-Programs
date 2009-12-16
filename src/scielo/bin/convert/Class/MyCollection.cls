VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "MyCollection"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"MyClass"
Attribute VB_Ext_KEY = "Member0" ,"MyClass"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable to hold collection
Private mCol As Collection
Public isobj As Boolean

Public Sub Add(objNewMember, Optional SKEY As String)

    If Len(SKEY) = 0 Then
        mCol.Add objNewMember
    Else
        mCol.Add objNewMember, SKEY
    End If
End Sub

Public Property Get Item(vntIndexKey As Variant, Optional exist As Boolean) As Variant
Attribute Item.VB_UserMemId = 0
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
    On Error GoTo NoExist
    
    If isobj Then
        Set Item = Nothing
        Set Item = mCol(vntIndexKey)
        exist = True
    Else
        Item = mCol(vntIndexKey)
        exist = True
    End If
    
    Exit Property
NoExist:
    exist = False
    If isobj Then Set Item = Nothing
End Property



Public Property Get Count() As Long
    'used when retrieving the number of elements in the
    'collection. Syntax: 'Debug.Print x.Count
    Count = mCol.Count
End Property


Public Function Remove(vntIndexKey As Variant) As Boolean
    'used when removing an element from the collection
    'vntIndexKey contains either the Index or Key, which is why
    'it is declared as a Variant
    'Syntax: x.Remove(xyz)
    Dim existe As Boolean
    
    IsObject (Item(vntIndexKey, existe))
    If existe Then mCol.Remove vntIndexKey
    Remove = existe
End Function


Public Property Get NewEnum() As IUnknown
Attribute NewEnum.VB_UserMemId = -4
Attribute NewEnum.VB_MemberFlags = "40"
    'this property allows you to enumerate
    'this collection with the for...Each syntax
    Set NewEnum = mCol.[_NewEnum]
End Property


Private Sub Class_Initialize()
    'creates the collection when this class is created
    Set mCol = New Collection
End Sub


Private Sub Class_Terminate()
    'destroys collection when this class is terminated
    Set mCol = Nothing
End Sub

