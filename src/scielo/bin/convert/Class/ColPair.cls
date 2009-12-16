VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColPair"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"ClPair"
Attribute VB_Ext_KEY = "Member0" ,"ClPair"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable to hold collection
Private mCol As Collection
Public key As String
Private keylist As New ColPair

Public Function Add(SKEY As String) As ClPair
    'create a new object
    Dim objNewMember As ClPair
    
    Set objNewMember = New ClPair
    
    'set the properties passed into the method
    If Len(SKEY) = 0 Then
        mCol.Add objNewMember
    Else
        mCol.Add objNewMember, SKEY
    End If
    
    'return the object created
    Set Add = objNewMember
    Set objNewMember = Nothing


End Function

Public Function AddBin(SKEY As String, elem1 As String) As ClPair
    'create a new object
    Dim objNewMember As ClPair
    Dim aux As ClPair
    Dim existbin As Boolean
    Dim existtxt As Boolean
    Dim i As Long
    Dim k As String
    Dim itemKey As ClPair
    
    Set objNewMember = New ClPair
    Set aux = New ClPair
    Set itemKey = New ClPair
    
    'set the properties passed into the method
    If Len(SKEY) = 0 Then
        mCol.Add objNewMember
    Else
        k = SKEY
        Set aux = ItemBin(k, elem1, existbin)
        If Not existbin Then
            Set itemKey = keylist.Item(SKEY, existtxt)
            If existtxt Then
                k = SKEY + itemKey.elem2
                mCol.Add objNewMember, k
                itemKey.elem2 = CStr(CLng(itemKey.elem2) + 1)
            Else
                Set itemKey = keylist.Add(SKEY)
                k = SKEY + itemKey.elem2
                mCol.Add objNewMember, k
                itemKey.elem2 = "1"
            End If
        End If
    End If
    
    'return the object created
    Set AddBin = objNewMember
    Set objNewMember = Nothing


End Function

Public Property Get Item(vntIndexKey As Variant, Optional exist As Boolean) As ClPair
Attribute Item.VB_UserMemId = 0
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
  On Error GoTo notexist
  Set Item = mCol(vntIndexKey)
  exist = True
  Exit Property
notexist:
    Set Item = Nothing
    exist = False
End Property

Public Property Get ItemBin(vntIndexKey As String, elem1 As String, existbin As Boolean) As ClPair
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.ItemBin(xyz) or Set foo = x.ItemBin(5)
    Dim i As Long
    'Dim ItemBin As ClPair
    Dim key As String
    Dim Key2 As String
    Dim k As ClPair
    Dim exist As Boolean
     
    On Error GoTo notexist
    
    
    key = vntIndexKey
    existbin = False
    Set k = New ClPair
    Set k = keylist.Item(key, exist)
    If exist Then
        While (Not existbin) And (i < CLng(k.elem2))
            i = i + 1
            Key2 = key + CStr(i)
            Set ItemBin = mCol(Key2)
            If StrComp(ItemBin.elem1, elem1, vbBinaryCompare) = 0 Then
                existbin = True
            End If
        Wend
    Else
        Set ItemBin = Nothing
        existbin = False
    End If
  Exit Property
notexist:
    Set ItemBin = Nothing
    existbin = False
End Property

Public Property Get Count() As Long
    'used when retrieving the number of elements in the
    'collection. Syntax: Debug.Print x.Count
    Count = mCol.Count
End Property


Public Sub Remove(vntIndexKey As Variant)
    'used when removing an element from the collection
    'vntIndexKey contains either the Index or Key, which is why
    'it is declared as a Variant
    'Syntax: x.Remove(xyz)


    mCol.Remove vntIndexKey
End Sub


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
    'Set keylist = new ColPair
End Sub


Private Sub Class_Terminate()
    'destroys collection when this class is terminated
    Set mCol = Nothing
    Set keylist = Nothing
End Sub

