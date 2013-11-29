VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColLicenses"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Private mCol As Collection

Sub load(licenses_from_codedb As ColObjByLang)

    Dim license As clsCreativeCommons
    Dim i_lictype As Long
    Dim i_lang As Long
    Dim default_licenses As ColCode
    Dim license_texts As clsCreativeCommons
    
    
    Set default_licenses = licenses_from_codedb.getItemByIndex(1)
    
    For i_lictype = 1 To default_licenses.count
        Set license_texts = New clsCreativeCommons
        license_texts.Code = default_licenses.item(i_lictype).Code
        
        For i_lang = 1 To licenses_from_codedb.count
        
            Call license_texts.add(licenses_from_codedb.getItemByIndex(i_lang).item(license_texts.Code).value, licenses_from_codedb.getItemByIndex(i_lang).lang)
        Next
        Call add(license_texts, license_texts.Code)
    Next

End Sub
Function isCustomizedLicense(lic As clsCreativeCommons) As Boolean
    Dim license As clsCreativeCommons
    Dim i As Long
    Dim changed As Boolean
    
    If lic.Code <> "" Then
        Set license = item(lic.Code)
        i = 1
        While (i <= license.count) And (Not changed)
            changed = Not (license.getLicenseByIndex(i).text = lic.getLicense(license.getLicenseByIndex(i).lang).text)
            i = i + 1
        Wend
    End If
    isCustomizedLicense = changed
End Function

Function isEqual(lic As clsCreativeCommons, license As clsCreativeCommons) As Boolean
     Dim i As Long
    Dim is_eq As Boolean
    
    If lic.Code = license.Code Then
        is_eq = True
        i = 1
        While (i <= license.count) And (is_eq)
            is_eq = (license.getLicenseByIndex(i).text = lic.getLicense(license.getLicenseByIndex(i).lang).text)
            i = i + 1
        Wend
    End If
    isEqual = is_eq
End Function
Public Function add(obj As clsCreativeCommons, SKEY As String) As clsCreativeCommons
    
    Call mCol.add(obj, SKEY)
    Set add = obj


End Function

Public Property Get item(vntIndexKey As Variant, Optional exist As Boolean) As clsCreativeCommons
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
        If StrComp(vntIndexKey, mCol(i).value, vbTextCompare) = 0 Then
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


