VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClIdiomMeses"
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
Private mvarMeses As New ColMeses  'local copy
Private mvarChIdioma As String 'local copy
Private mvarIndice As Long 'local copy
Public Property Let Indice(ByVal vData As Long)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Indice = 5
    mvarIndice = vData
End Property


Public Property Get Indice() As Long
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Indice
    Indice = mvarIndice
End Property



Public Property Let ChIdioma(ByVal vData As String)
    On Error GoTo ChIdiomaLetErr


'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.ChIdioma = 5
    mvarChIdioma = vData
    Exit Property


ChIdiomaLetErr:


    Call RaiseError(MyUnhandledError, "ClIdiomMeses:ChIdioma Property Let")
End Property


Public Property Get ChIdioma() As String
    On Error GoTo ChIdiomaGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.ChIdioma
    ChIdioma = mvarChIdioma
    Exit Property


ChIdiomaGetErr:


    Call RaiseError(MyUnhandledError, "ClIdiomMeses:ChIdioma Property Get")
End Property



Public Property Set Meses(ByVal vData As Object)
    On Error GoTo MesesSetErr


'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.Meses = Form1
    Set mvarMeses = vData
    Exit Property


MesesSetErr:


    Call RaiseError(MyUnhandledError, "ClIdiomMeses:Meses Property Set")
End Property


Public Property Get Meses() As ColMeses
    On Error GoTo MesesGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Meses
    Set Meses = mvarMeses
    Exit Property


MesesGetErr:


    Call RaiseError(MyUnhandledError, "ClIdiomMeses:Meses Property Get")
End Property





Private Sub Class_Initialize()
    #If DebugMode Then
        'get the next available class ID, and print out
        'that the class was created successfully
        mlClassDebugID = GetNextClassDebugID()
        Debug.Print "'" & TypeName(Me) & "' instance " & mlClassDebugID & " created"
    #End If
End Sub


Private Sub Class_Terminate()
    'the class is being destroyed
    #If DebugMode Then
        Debug.Print "'" & TypeName(Me) & "' instance " & CStr(mlClassDebugID) & " is terminating"
    #End If
End Sub


#If DebugMode Then
    Public Property Get ClassDebugID()
        'if we are in debug mode, surface this property that consumers can query
        ClassDebugID = mlClassDebugID
    End Property
#End If

