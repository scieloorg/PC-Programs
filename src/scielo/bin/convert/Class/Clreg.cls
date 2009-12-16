VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClRegistro"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public InfoFields As ColField
Public fields As ColField
Public Tipo As String 'local copy
Public Id As String 'local copy

Private privateContent As ClContent


Private Sub Class_Initialize()
    Set fields = New ColField
    Set InfoFields = New ColField
    Set privateContent = New ClContent
End Sub

Private Sub Class_Terminate()
    Set fields = Nothing
    Set InfoFields = Nothing
End Sub

Function conteudo() As String
    Dim i As Long
    Dim content As String
    
    For i = 1 To InfoFields.Count
        content = content + TagContent(InfoFields(i).conteudo, InfoFields(i).Campo)
    Next
    For i = 1 To fields.Count
        content = content + TagContent(fields(i).conteudo, fields(i).Campo)
    Next
    conteudo = content
End Function

Private Function TagContent(ByVal conteudo As String, ByVal Tag As Long) As String
    TagContent = privateContent.TagContent(conteudo, Tag)
End Function

Function OccNumber(Field As Long, content() As String) As Long
    Dim i As Long
    Dim n As Long
    
    For i = 1 To fields.Count
        If fields(i).Campo = Field Then
            n = n + 1
            ReDim Preserve content(n)
            content(n) = fields(i).conteudo
        End If
    Next
    OccNumber = n
End Function

Sub DelFields(Field As Long)
    Dim i As Long
    
    i = 1
    While (i < fields.Count)
    
        If fields(i).Campo = Field Then
            fields.Remove (i)
        Else
            i = i + 1
        End If
    Wend
End Sub

Function Copy() As ClRegistro
    Dim r As ClRegistro
    Dim i As Long
    
    Set r = New ClRegistro
    For i = 1 To InfoFields.Count
        With InfoFields(i)
        Call r.InfoFields.Add(.key, .Campo, .conteudo, .Tipo, .Id)
        End With
    Next
    For i = 1 To fields.Count
        With fields(i)
        Call r.fields.Add(.key, .Campo, .conteudo, .Tipo, .Id)
        End With
    Next
    r.Tipo = Tipo
    r.Id = Id
    
    Set Copy = r
    Set r = Nothing
End Function
