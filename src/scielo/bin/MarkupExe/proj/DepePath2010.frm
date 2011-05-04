VERSION 5.00
Begin VB.Form DepePath 
   Caption         =   "Finding WORD97"
   ClientHeight    =   3195
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   5325
   LinkTopic       =   "Form1"
   ScaleHeight     =   3195
   ScaleWidth      =   5325
   StartUpPosition =   3  'Windows Default
   Begin VB.CommandButton Command2_Can 
      Caption         =   "Cancel"
      Height          =   495
      Left            =   3000
      TabIndex        =   4
      Top             =   2520
      Width           =   1335
   End
   Begin VB.CommandButton Command1_OK 
      Caption         =   "OK"
      Height          =   495
      Left            =   1080
      TabIndex        =   3
      Top             =   2520
      Width           =   1335
   End
   Begin VB.TextBox Text1 
      Height          =   615
      Left            =   240
      TabIndex        =   2
      Top             =   1680
      Width           =   4935
   End
   Begin VB.Label Label2_Prompt 
      Caption         =   "Write the right path to find the archive ""winword.exe"""
      Height          =   495
      Left            =   240
      TabIndex        =   1
      Top             =   840
      Width           =   4815
   End
   Begin VB.Label Label1_Prompt 
      Caption         =   "Not found the archive  ""winword.exe"""
      Height          =   375
      Left            =   240
      TabIndex        =   0
      Top             =   240
      Width           =   4815
   End
End
Attribute VB_Name = "DepePath"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Command1_OK_Click()
    'recebe caminho indicado pelo usuário e armazena
    'no arquivo start.mds
    'Dim conf As New clsConfig
    '------------------------
    'conf.LoadPublicValues
    
    path = DepePath.Text1.Text
    Open App.path & "\start.mds" For Output As #1
    Write #1, path
    Close #1
    
    'caso ainda nao encontre continua no mesmo form
    On Error GoTo volta
    'executa o WORD97 chamando a macro que prepara o ambiente
    'de marcacao. O caminho é o indicado pelo usuário
    callWord (path)
    
    Unload DepePath
    DepePath.Hide
    'Set conf = Nothing
    End
volta:
    MsgBox "Not found. Type the right path.", vbCritical, "Error to find the archive"
    'Set conf = Nothing
End Sub


Private Sub Command2_Can_Click()
    MsgBox "Confirm the path to find the archive winword.exe", vbCritical, "Error to load"
    Unload DepePath
    DepePath.Hide
    End
End Sub

