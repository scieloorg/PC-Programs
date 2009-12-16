VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColProc"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"ClProc"
Attribute VB_Ext_KEY = "Member0" ,"ClProc"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
'local variable to hold collection
Private mCol As Collection


Public Function Add(key As String) As ClProc
    'create a new object
    Dim objNewMember As ClProc
    Set objNewMember = New ClProc


    If Len(key) = 0 Then
        mCol.Add objNewMember
    Else
        mCol.Add objNewMember, key
    End If


    'return the object created
    Set Add = objNewMember
    Set objNewMember = Nothing


End Function

Public Property Get Item(vntIndexKey As Variant, Optional exist As Boolean) As ClProc
Attribute Item.VB_UserMemId = 0
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
    On Error GoTo NoExist
    Set Item = mCol(vntIndexKey)
    exist = True
    Exit Property
NoExist:
    exist = False
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
End Sub


Private Sub Class_Terminate()
    'destroys collection when this class is terminated
    Set mCol = Nothing
End Sub


Sub CreateMstModels(dbname As String)

    Dim i As Long
    Dim fn As Long
    Dim isatt As String
    
    fn = FreeFile
    Open dbname For Output As fn
    
    For i = 1 To Count
        With Item(i)
        If .is_attribute Then
            isatt = "1"
        Else
            isatt = ""
        End If
        
        Print #fn, .key + "|" + .sgmltag + "|" + isatt + "|" + .LINKBY_FATHER + "|" + .LINKBY_INDEX + "|" + .LINKBY_CROSSREFERENCE + "|" + .LINKBY_FATHER2 + .params.CreateMst
        End With
    Next
    
    Close fn
End Sub
