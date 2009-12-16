VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClTabCol"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'set this to 0 to disable debug code in this class
#Const DebugMode = 1


#If DebugMode Then
    'local variable to hold the serialized class ID that was created in Class_Initialize
    Private mlClassDebugID As Long
#End If

Private mvarLinha() As Variant 'local copy
Private mvarCounter As Long 'local copy
Private mvarIdx As Long 'local copy
Private mvarName As String 'local copy
Private Chaves As MyCollection


Public Property Let name(ByVal vData As String)
    On Error GoTo NameLetErr


'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Name = 5
    mvarName = vData
    Exit Property


NameLetErr:


    Call RaiseError(MyUnhandledError, "ClTabCol:Name Property Let")
End Property


Public Property Get name() As String
    On Error GoTo NameGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Name
    name = mvarName
    Exit Property


NameGetErr:


    Call RaiseError(MyUnhandledError, "ClTabCol:Name Property Get")
End Property



Public Property Let idx(ByVal vData As Long)
    On Error GoTo IdxLetErr


'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Idx = 5
    mvarIdx = vData
    Exit Property


IdxLetErr:


    Call RaiseError(MyUnhandledError, "ClTabCol:Idx Property Let")
End Property


Public Property Get idx() As Long
    On Error GoTo IdxGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Idx
    idx = mvarIdx
    Exit Property


IdxGetErr:


    Call RaiseError(MyUnhandledError, "ClTabCol:Idx Property Get")
End Property



Public Property Let counter(ByVal vData As Long)
    On Error GoTo CounterLetErr


'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Counter = 5
    mvarCounter = vData
    ReDim Preserve mvarLinha(mvarCounter)
    Exit Property


CounterLetErr:


    Call RaiseError(MyUnhandledError, "ClTabCol:Counter Property Let")
End Property


Public Property Get counter() As Long
    On Error GoTo CounterGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Counter
    counter = mvarCounter
    Exit Property


CounterGetErr:


    Call RaiseError(MyUnhandledError, "ClTabCol:Counter Property Get")
End Property



Public Property Let Linha(idx As Long, ByVal vData As Variant)
    Dim exist As Boolean
    Dim aux As String
    Dim Key As String
    
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Linha = 5
    Key = CStr(vData)
    If idx > counter Then counter = idx
    
    aux = Chaves.Item(Key, exist)
    If exist Then
        Chaves.Remove (Key)
        Call Chaves.Add(aux + COMMA_DUVIDA + CStr(idx), Key)
    Else
        Call Chaves.Add(CStr(idx), Key)
    End If
    mvarLinha(idx) = vData
End Property



Public Property Get Linha(idx As Long) As Variant
    On Error GoTo LinhaGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Linha
    If (idx > 0) And (idx <= counter) Then Linha = mvarLinha(idx)
    Exit Property


LinhaGetErr:


    Call RaiseError(MyUnhandledError, "ClTabCol:Linha Property Get")
End Property





Private Sub Class_Initialize()
    #If DebugMode Then
        'get the next available class ID, and print out
        'that the class was created successfully
        mlClassDebugID = GetNextClassDebugID()
        'Debug.Print "'" & TypeName(Me) & "' instance " & mlClassDebugID & " created"
    #End If
    Set Chaves = New MyCollection
End Sub


Private Sub Class_Terminate()
    'the class is being destroyed
    #If DebugMode Then
        'Debug.Print "'" & TypeName(Me) & "' instance " & CStr(mlClassDebugID) & " is terminating"
    #End If
    Set Chaves = Nothing
End Sub


#If DebugMode Then
    Public Property Get ClassDebugID()
        'if we are in debug mode, surface this property that consumers can query
        ClassDebugID = mlClassDebugID
    End Property
#End If

'-----------------------------------------------------------------------
'FindText   - encontra um termo (comparação textual) em uma determinada coluna
'Linhas     - índices das linhas em que foram encontrados os termos
'Retorno    - quantidade de termos encontrados
'-----------------------------------------------------------------------
Function FindText(Termo As String, linhas() As Long) As Long
    Dim idx() As String
    Dim i As Long
    Dim Qtd As Long
    Dim aux As String
    Dim exist As Boolean
    
    aux = Chaves.Item(Termo, exist)
    
    If exist Then
        Qtd = GetElemStr(aux, COMMA_DUVIDA, idx)
        ReDim linhas(Qtd)
        For i = 1 To Qtd
            linhas(i) = CLng(idx(i))
        Next
    Else
        Erase linhas
    End If
    FindText = Qtd
End Function

'-----------------------------------------------------------------------
'FindBin   - encontra um termo (comparação binária) em uma determinada coluna
'Linhas     - índices das linhas em que foram encontrados os termos
'Retorno    - quantidade de termos encontrados
'-----------------------------------------------------------------------
Function FindBin(Termo As String, linhas() As Long) As Long
    Dim idx() As String
    Dim i As Long
    Dim Qtd As Long
    Dim aux As String
    Dim exist As Boolean
    Dim j As Long
    
    aux = Chaves.Item(Termo, exist)
    If exist Then
        Qtd = GetElemStr(aux, COMMA_DUVIDA, idx)
        ReDim linhas(Qtd)
        For i = 1 To Qtd
            If StrComp(Linha(CLng(idx(i))), Termo, vbBinaryCompare) = 0 Then
                j = j + 1
                linhas(j) = CLng(idx(i))
            End If
        Next
        ReDim Preserve linhas(j)
        Qtd = j
    Else
        Erase linhas
    End If
    FindBin = Qtd
End Function

'-----------------------------------------------------------------------
'Find   - encontra um termo em uma determinada coluna
'Linhas     - índices das linhas em que foram encontrados os termos
'Retorno    - quantidade de termos encontrados
'CmdType    - tipo de comparação
'-----------------------------------------------------------------------
Function Find(Termo As String, linhas() As Long, CmpType As VbCompareMethod) As Long
    Dim idx() As String
    Dim i As Long
    Dim Qtd As Long
    Dim aux As String
    Dim exist As Boolean
    Dim j As Long
    
    aux = Chaves.Item(Termo, exist)
    If exist Then
        Qtd = GetElemStr(aux, COMMA_DUVIDA, idx)
        ReDim linhas(Qtd)
        
        Select Case CmpType
        Case vbTextCompare
            For i = 1 To Qtd
                linhas(i) = CLng(idx(i))
            Next

        Case vbBinaryCompare
            For i = 1 To Qtd
                If StrComp(Linha(CLng(idx(i))), Termo, vbBinaryCompare) = 0 Then
                    j = j + 1
                    linhas(j) = CLng(idx(i))
                End If
            Next
            ReDim Preserve linhas(j)
            Qtd = j
        End Select
    Else
        Erase linhas
    End If
    Find = Qtd
End Function


