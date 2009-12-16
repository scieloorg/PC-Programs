VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClTitleDB"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"


Option Explicit

Private BD As ClIsisDll
Private title As ClIsisDll

Private SerialTitles() As String
Private k As Long

Property Get PathTitles() As String
    PathTitles = BD.BDPath
End Property
Property Let PathTitles(v As String)
    BD.BDPath = v
End Property
Property Get ArqTitles() As String
    ArqTitles = BD.BDNome
End Property
Property Let ArqTitles(v As String)
    BD.BDNome = v
End Property
Property Get ArqInvert() As String
    ArqInvert = BD.IfName
End Property
Property Let ArqInvert(v As String)
    BD.IfName = v
End Property
Property Get BDTitle() As ClIsisDll
    Set BDTitle = BD
End Property
Property Set BDTitle(v As ClIsisDll)
    Set BD = v
End Property

Function Inicia(Path As String, base As String, Invert As String, OnlyTitles As String) As Boolean
    Dim ret As Boolean
    Set BD = New ClIsisDll
    If BD.Inicia(Path, base, "Database Title") Then
        If BD.IfCreate(Invert) Then
            If BD.MfnQuantity > 0 Then
                Call BD.IfUpdate(1, BD.MfnQuantity)
                Call GetSerialTitles(Path, base, OnlyTitles)
            End If
            ret = True
        End If
    End If
    
    Inicia = ret
End Function

Private Sub GetSerialTitles(Path As String, base As String, Invert As String)
    k = 0
    Erase SerialTitles
    Set title = New ClIsisDll
    If title.Inicia(Path, base, "Database Title") Then
        If title.IfCreate(Invert) Then
            If title.MfnQuantity > 0 Then
                Call title.IfUpdate(1, title.MfnQuantity)
                k = title.GetTerms(SerialTitles, "v130*0.1|:|,v100")
            End If
        End If
    End If
    'Set title = Nothing
End Sub

Property Get SerialTitle(i As Long) As String
    If (i > 0) And (i <= k) Then
        SerialTitle = SerialTitles(i)
    Else
        SerialTitle = ""
    End If
End Property

Property Get SerialCount() As Long
    SerialCount = k
End Property

Private Sub Class_Terminate()
    Set BD = Nothing
    Set title = Nothing
End Sub

Function GetFieldContents(Key As String, Field As Long, Contents() As String) As Long
    Dim q As Long
    
    q = BDTitle.FieldContentGet(BDTitle.MfnFindOne(Key), Field, Contents)
    GetFieldContents = q
End Function

