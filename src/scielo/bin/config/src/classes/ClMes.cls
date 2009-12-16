VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClMes"
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
'local variable(s) to hold property value(s)
Private mvarmes As String 'local copy
Private mvarIndice As Long 'local copy
Public Property Let Indice(ByVal vData As Long)
    On Error GoTo indiceLetErr


'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.indice = 5
    mvarIndice = vData
    Exit Property


indiceLetErr:


    Call RaiseError(MyUnhandledError, "ClMes:indice Property Let")
End Property

Public Property Get Indice() As Long
    On Error GoTo indiceGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.indice
    Indice = mvarIndice
    Exit Property


indiceGetErr:


    Call RaiseError(MyUnhandledError, "ClMes:indice Property Get")
End Property

Public Property Let mes(ByVal vData As String)
    On Error GoTo MesLetErr


'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Mes = 5
    mvarmes = vData
    Exit Property


MesLetErr:


    Call RaiseError(MyUnhandledError, "ClMes:Mes Property Let")
End Property

Public Property Get mes() As String
    On Error GoTo MesGetErr


'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Mes
    mes = mvarmes
    Exit Property


MesGetErr:


    Call RaiseError(MyUnhandledError, "ClMes:Mes Property Get")
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

