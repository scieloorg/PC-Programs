VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColRegistro"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"ClRegistro"
Attribute VB_Ext_KEY = "Member0" ,"ClRegistro"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Attribute VB_Ext_KEY = "Member1" ,"ClRegistro"
Attribute VB_Ext_KEY = "Member2" ,"ClRegistro"
Attribute VB_Ext_KEY = "Member3" ,"ClRegistro"
Attribute VB_Ext_KEY = "Member4" ,"ClRegistro"
Attribute VB_Ext_KEY = "Member5" ,"ClRegistro"
Attribute VB_Ext_KEY = "Member6" ,"ClRegistro"
Attribute VB_Ext_KEY = "Member7" ,"ClRegistro"
'local variable to hold collection
Private mCol As Collection

Private CurrKey As Long

Public Function Add(Optional SKEY As String, Optional Tipo As String, Optional Id As Long, Optional newitem As ClRegistro) As ClRegistro
    'create a new object
    Dim objNewMember As ClRegistro
    
    On Error GoTo erro
    Set objNewMember = New ClRegistro
    If newitem Is Nothing Then
        'set the properties passed into the method
        objNewMember.Tipo = Tipo
        objNewMember.Id = Id
    Else
        Set objNewMember = newitem
    End If
    
    If Len(SKEY) = 0 Then
        mCol.Add objNewMember
    Else
        mCol.Add objNewMember, SKEY
    End If


    'return the object created
    Set Add = objNewMember
    Set objNewMember = Nothing
Exit Function
erro:
'Debug.Print

End Function

Public Property Get Item(vntIndexKey As Variant, Optional existe As Boolean) As ClRegistro
Attribute Item.VB_UserMemId = 0
    'used when referencing an element in the collection
    'vntIndexKey contains either the Index or Key to the collection,
    'this is why it is declared as a Variant
    'Syntax: Set foo = x.Item(xyz) or Set foo = x.Item(5)
    On Error GoTo NaoExiste
    Set Item = mCol(vntIndexKey)
    existe = True
    Exit Property
NaoExiste:
    existe = False

End Property

Public Property Get Count() As Long
    'used when retrieving the number of elements in the
    'collection. Syntax: 'Debug.Print x.Count
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

Public Function GetLawRecord(key As String, element As String, root As String, fieldkey As String, rectype As String, status As String) As ClRegistro
    Dim LawStructElem As ClRegistro
    Dim existe As Boolean
    
    
    Set LawStructElem = New ClRegistro
        
    Set LawStructElem = Item(key, existe)
    
    'caso seja body or attach, as chaves devem ser reavaliadas
    If existe Then
        If StrComp(element, root, vbTextCompare) = 0 Then
            If Len(fieldkey) = 0 Then
                CurrKey = CurrKey + 1
            End If
            key = key + "_" + CStr(CurrKey)
        End If
    End If
    
    Set LawStructElem = Item(key, existe)
    
    ' cria registro
    ' preenche key, elemento, tipo e id do registro
    ' encontra hierarquia: nivel, pais, filhos
    If Not existe Then
        ' cria registro
        Set LawStructElem = Add(key)
        
        ' preenche key, elemento, tipo e id do registro
        With LawStructElem
        .Id = CStr(Count)
        .Tipo = rectype
        Call .fields.Add("200", 200, key)
        Call .fields.Add("204", 204, element)
        Call .fields.Add("999", 999, status)
        End With
    End If
    Set GetLawRecord = LawStructElem
    Set LawStructElem = Nothing
End Function

