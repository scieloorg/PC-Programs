VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ColBodyElem"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"ClBodyElem"
Attribute VB_Ext_KEY = "Member0" ,"ClBodyElem"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable to hold collection
Private mCol As Collection

Public Function Add(sKey As String) As ClBodyElem
    'create a new object
    Dim objNewMember As ClBodyElem
    Set objNewMember = New ClBodyElem


    'set the properties passed into the method
    objNewMember.Key = sKey
    Set objNewMember.Children = New ColBodyElem

    If Len(sKey) = 0 Then
        mCol.Add objNewMember
    Else
        mCol.Add objNewMember, sKey
    End If


    'return the object created
    Set Add = objNewMember
    Set objNewMember = Nothing


End Function

Public Property Get Item(vntIndexKey As Variant, Optional exist As Boolean) As ClBodyElem
Attribute Item.VB_UserMemId = 0
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
    
  On Error GoTo NoExist:
  Set Item = mCol(vntIndexKey)
  exist = True
  Exit Property
NoExist:
    exist = False
    Set Item = Nothing
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
    'this collection with the For...Each syntax
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

Public Sub Percorre(File As String, indent As Long)
    Dim i As Long
    Dim fn As Long
    
    For i = 1 To Count
        fn = 1
        Open File For Append As fn
        Print #fn, String(indent, "|") + Item(i).Key + "," + Item(i).parent.Key + "," + Item(i).name + "," + Item(i).no + "," + Item(i).content
        Close fn
        Debug.Print String(indent, "|") + Item(i).Key + "," + Item(i).parent.Key + "," + Item(i).name + "," + Item(i).no + "," + Item(i).content
        
        If Item(i).Children Is Nothing Then
        Else
            Call Item(i).Children.Percorre(File, indent + 1)
        End If
    Next
    
End Sub

Public Function BuildRecords(MBodyRecord As ColRegistro, CRCount As Long) As ColRegistro
    Dim i As Long
    Dim mbr As ClRegistro
    Dim content As String
    
    Debug.Print MBodyRecord.Count
    
    Set mbr = New ClRegistro
    For i = 1 To Count
        With Item(i)
        content = TagContents(.Path, 200)
        content = content + TagContents(.no, 201)
        content = content + TagContents(.name, 202)
        content = content + TagContents(.content, 203)
        content = content + TagContents(.Tp, 204)
        content = content + TagContents(.level, 205)
        content = content + .listParents(206)
        content = content + .listChildren(207)
        
        CRCount = CRCount + 1
        Set mbr = MBodyRecord.Add("c" + CStr(CRCount), , content, "c", CRCount)
        Set mbr = MBodyRecord.Add("r" + CStr(CRCount), , content, "r", CRCount)
        
        
        Set MBodyRecord = .Children.BuildRecords(MBodyRecord, CRCount)
        Debug.Print MBodyRecord.Count
        End With
    Next
    Set BuildRecords = MBodyRecord
End Function
