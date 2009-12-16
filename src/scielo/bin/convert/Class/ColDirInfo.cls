VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColDirInfo"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"ClDirInfo"
Attribute VB_Ext_KEY = "Member0" ,"ClDirInfo"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable to hold collection
Private mCol As Collection

Public Function Add(Optional Index As Long, Optional LabDir As String, Optional ObjTypeDir As String, Optional pattern As String, Optional ContentListFile As String, Optional level As Long, Optional Prefix As String, Optional suffix As String, Optional SKEY As String) As ClDirInfo
    'create a new object
    Dim objNewMember As ClDirInfo
    Set objNewMember = New ClDirInfo


    'set the properties passed into the method
    objNewMember.Index = Index
    objNewMember.LabDir = LabDir
    objNewMember.ObjTypeDir = ObjTypeDir
    objNewMember.pattern = pattern
    objNewMember.ContentListFile = ContentListFile
    objNewMember.level = level
    objNewMember.Prefix = Prefix
    objNewMember.suffix = suffix




    If Len(SKEY) = 0 Then
        mCol.Add objNewMember
    Else
        mCol.Add objNewMember, SKEY
    End If


    'return the object created
    Set Add = objNewMember
    Set objNewMember = Nothing


End Function

Public Property Get Item(vntIndexKey As Variant) As ClDirInfo
Attribute Item.VB_UserMemId = 0
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
  
  Set Item = mCol(vntIndexKey)
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


Public Function ReturnDataPath() As String
    Dim i As Long
    Dim level As String
    Dim level_content As String
    Dim Path As String
    Dim sep As String
    
    For i = 1 To Count
        With Item(i)
        If Len(.Value) > 0 Then
            If StrComp(level, .level, vbBinaryCompare) <> 0 Then
                'change level
                level = .level
                sep = PathSep
                level_content = ""
            Else
                sep = ""
            End If
            
            Select Case .optional_level
            Case "or"
                If Len(level_content) = 0 Then
                    level_content = .Prefix + .Value + .suffix
                    Path = Path + sep + level_content
                End If
            Case "and"
                Path = Path + sep + .Prefix + .Value + .suffix
            Case "ign"
            End Select
        End If
        End With
    Next
    
    ReturnDataPath = Path
End Function

Public Function ReturnDatabaseName() As String
    Dim i As Long
    Dim Id As String
    
    For i = 1 To Count
        With Item(i)
        If Len(.IsDatabaseName) > 0 Then
            If Len(.Value) > 0 Then Id = Id + .Prefix + .Value + .suffix
        End If
        End With
    Next
    If Len(Id) = 0 Then Id = GetDateISO(Date)
    
    ReturnDatabaseName = Id
End Function

Public Function ReturnDatabaseDir() As String
    Dim i As Long
    Dim Id As String
    
    For i = 1 To Count
        With Item(i)
        If Len(.IsDatabaseDir) > 0 Then
            If Len(.Value) > 0 Then Id = Id + .Prefix + .Value + .suffix
        End If
        End With
    Next
    If Len(Id) = 0 Then Id = GetDateISO(Date)
    
    ReturnDatabaseDir = Id
End Function

'-------------------------------------------------------------------------------------
'ReturnCfgRecKey - retorna a chave do registro de configuracao na base de configuracao,
'                   se existir
'-------------------------------------------------------------------------------------
Public Function ReturnCfgRecKey() As String
    Dim i As Long
    Dim ret As String
    
    For i = 1 To Count
        With Item(i)
        If Len(.cfgkey_pft) > 0 Then
            ret = ret + .CfgKeys(.cfgkey_key).elem2
        End If
        If Len(.cfgkey_val) > 0 Then
            If Len(.Value) > 0 Then ret = ret + .Prefix + .Value + .suffix
        End If
        End With
    Next
    ReturnCfgRecKey = ret
End Function

