VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClISSNDB"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public key As String
Public ISSN_tag As Long
Private sertitle_tags() As Long
Public SertitleCount As Long
Public StandardSertitle_tag As Long
Public FST_File_key As String

Property Get sertitle_tag(i As Long) As Long
    If i <= SertitleCount Then
        sertitle_tag = sertitle_tags(i)
    End If
End Property

Property Let sertitle_tag(i As Long, Tag As Long)
    If i > SertitleCount Then
        SertitleCount = i
        ReDim Preserve sertitle_tags(i)
    End If
    sertitle_tags(i) = Tag
End Property


Function MatchISSN1(Sertitle_tofind As String, rStandardSertitle As String, rISSN As String) As Boolean
    Dim Database As ClIsisDll
    Dim SertitleMfnCount As Long
    Dim SertitleMfns() As Long
    Dim ISSNCount As Long
    Dim ISSNs() As String
    Dim Sertitles() As String
    Dim k As Long
    Dim j As Long
    Dim found As Boolean
    
    Set Database = New ClIsisDll
                    
    With Database
    If .Initiate(BV(Currbv).FileTree.DirNodes(key).fullpath, BV(Currbv).FileTree.DirNodes(key).text, key) Then
        If .IfCreate(BV(Currbv).FileTree.DirNodes(FST_File_key).text, BV(Currbv).FileTree.DirNodes(key).key) Then
            SertitleMfnCount = .MfnFind(Sertitle_tofind, SertitleMfns)
            
            If SertitleMfnCount > 0 Then
                j = 0
                While (j < SertitleMfnCount) And (Not found)
                    j = j + 1
                    k = 0
                    While (k < SertitleCount) And (Not found)
                        k = k + 1
                        If StrComp(Sertitle_tofind, .FieldContentOccGet(SertitleMfns(j), sertitle_tag(k), 1), vbTextCompare) = 0 Then
                            found = True
                        End If
                    Wend
                Wend
            End If
            
            If found Then
                'obtem o valor do ISSN e do titulo standard
                ISSNCount = .FieldContentGet(SertitleMfns(j), ISSN_tag, ISSNs)
                If ISSNCount > 0 Then
                    rISSN = ISSNs(1)
                    SertitleCount = .FieldContentGet(SertitleMfns(j), StandardSertitle_tag, Sertitles)
                    If SertitleCount > 0 Then
                        rStandardSertitle = Sertitles(1)
                    Else
                        rStandardSertitle = Sertitle_tofind
                    End If
                End If
            End If
            
        End If
    End If
    End With
    Set Database = Nothing
    MatchISSN1 = found
End Function


Function AddTitleWithoutISSN(Sertitle_tofind As String) As Boolean
    Dim Database As ClIsisDll
    Dim SertitleMfnCount As Long
    Dim SertitleMfns() As Long
    Dim Sertitles() As Long
    Dim k As Long
    Dim j As Long
    Dim found As Boolean
    Dim ret As Boolean
    Dim MfnNOISSN As Long

    
    Set Database = New ClIsisDll
                    
    With Database
    If .Initiate(BV(Currbv).FileTree.DirNodes(key).fullpath, BV(Currbv).FileTree.DirNodes(key).text, BV(Currbv).FileTree.DirNodes(key).key) Then
        If .IfCreate(BV(Currbv).FileTree.DirNodes(key).text, BV(Currbv).FileTree.DirNodes(key).key) Then
            SertitleMfnCount = .MfnFind(Sertitle_tofind, SertitleMfns)
            
            If SertitleMfnCount > 0 Then
                j = 0
                While (j < SertitleMfnCount) And (Not found)
                    j = j + 1
                    k = 0
                    While (k < SertitleCount) And (Not found)
                        k = k + 1
                        If StrComp(Sertitle_tofind, .FieldContentOccGet(SertitleMfns(j), sertitle_tag(k), 1), vbTextCompare) = 0 Then
                            found = True
                        End If
                    Wend
                Wend
            End If
            
            If Not found Then
                
                MfnNOISSN = .RecordSave(.TagContents(Sertitle_tofind, sertitle_tag(1)))
                If MfnNOISSN > 0 Then
                    Call .IfUpdate(MfnNOISSN, MfnNOISSN)
                    ret = True
                    'MfnNOISSN = NoSertitleDB.MfnFind(Sertitle, SertitleMfn)
                    
                End If
                
            End If
        End If
    End If
    End With
    Set Database = Nothing
    AddTitleWithoutISSN = ret
End Function
