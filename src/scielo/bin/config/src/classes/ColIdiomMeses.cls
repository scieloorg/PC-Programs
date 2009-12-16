VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ColIdiomMeses"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Collection" ,"ClIdiomMeses"
Attribute VB_Ext_KEY = "Member0" ,"ClIdiomMeses"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'local variable to hold collection
Private mCol As Collection

Function ReadMonthTable() As Boolean
    Dim s As String
    Dim i As Long
    Dim j As Long
    Dim fn As Long
    Dim Info() As String
    Dim Code As String
    Dim Months As String
    Dim ListMonths As ColMeses
    Dim Ret As Boolean
    
    With Paths("Month Table")
    If FileExist(.path, .filename, .key) Then
        Ret = True
        fn = FreeFile(1)
        Open .path + "\" + .filename For Input As fn
        While Not EOF(fn)
            Line Input #fn, s
            j = GetElemStr(s, ",", Info)
            If j = 2 Then
                Code = Info(1)
                Months = Info(2)
                j = GetElemStr(Months, ",", Info)
                
                Set ListMonths = New ColMeses
                For i = 1 To j
                    Call ListMonths.Add(Info(i), i, Info(i))
                Next
                Ret = Ret And True
                Call Add(ListMonths, Code, Code)
            Else
                Ret = False
            End If
        Wend
    End If
    End With
    ReadMonthTable = Ret
End Function

Function GetMonth(Idioma As String, DateISO As String, FREQCODE As String) As String
    Dim i As Long
    Dim sep As String
    Dim existe As Boolean
    Dim FIRSTMONTH As Long
    Dim LASTMONTH As Long
    Dim m As ClMes
    Dim MONTHISO As String
    Dim MONTHBIBSTRIP As String
    Dim Months As Long
    Dim DAYS As Long
    Dim YEARS As Long
    
    
    MONTHISO = Mid(DateISO, 5, 2)
    If Len(MONTHISO) = 0 Then MONTHISO = "00"
    If StrComp(MONTHISO, "00") = 0 Then
        FIRSTMONTH = 0
        LASTMONTH = 0
    Else
        
        Select Case FREQCODE
        Case "M"
            Months = 1
        Case "B"
            Months = 2
        Case "Q"
            Months = 3
        Case "T"
            Months = 4
        Case "F"
            Months = 6
        Case "K", "Z"
            DAYS = 0
        Case "D"
            DAYS = 1
        Case "I"
            DAYS = 2
        Case "C"
            DAYS = 3
        Case "W"
            DAYS = 7
        Case "J"
            DAYS = 10
        Case "E"
            DAYS = 14
        Case "S"
            DAYS = 15
        Case "A"
            YEARS = 1
        Case "G"
            YEARS = 2
        Case "H"
            YEARS = 3
        End Select
    
        FIRSTMONTH = CLng(MONTHISO)
        LASTMONTH = FIRSTMONTH + Months - 1
        If LASTMONTH > 12 Then
            LASTMONTH = LASTMONTH - 12
        End If
    
        Set m = New ClMes
        Set m = Item(Idioma).Meses.Item(FIRSTMONTH, existe)
        If existe Then MONTHBIBSTRIP = m.mes
        'If FIRSTMONTH <> LASTMONTH Then
        '    Set m = Item(Idioma).Meses.Item(LASTMONTH, existe)
        '    If existe Then MONTHBIBSTRIP = MONTHBIBSTRIP + "/" + m.mes
        'End If
        
    End If
    
    
    GetMonth = MONTHBIBSTRIP
End Function



Function MonthCount() As Long
    MonthCount = Item(1).Meses.Count
End Function


Public Function Add(Optional Meses As ColMeses, Optional ChIdioma As String, Optional SKEY As String) As ClIdiomMeses
    'create a new object
    Dim objNewMember As ClIdiomMeses
    Set objNewMember = New ClIdiomMeses

    'set the properties passed into the method
    Set objNewMember.Meses = Meses
    objNewMember.ChIdioma = ChIdioma

    If Len(SKEY) = 0 Then
        mCol.Add objNewMember
    Else
        mCol.Add objNewMember, SKEY
    End If

    'return the object created
    Set Add = objNewMember
    Set objNewMember = Nothing

End Function

Public Property Get Item(vntIndexKey As Variant) As ClIdiomMeses
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

Private Sub Class_Initialize()
    'creates the collection when this class is created
    Set mCol = New Collection
End Sub

Private Sub Class_Terminate()
    'destroys collection when this class is terminated
    Set mCol = Nothing
End Sub

