VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClDirInfo"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"

Option Explicit


Public Index As Long    'indice da linha
Public LabDir As String 'key of the label in InterfaceLabels
Public ObjTypeDir As String 'tipo do campo (textbox, combobox)
Public pattern As String    'padrao do preenchimento
Public ContentListFile As String    'Arquivo com a lista para o combobox
Public ContentListAbbr As ColPair   'Lista de conteudo do combobox: abreviado
Public ContentListFull As ColPair   'Lista de conteudo do combobox: completo
Public CfgKeys As ColPair       '
Public DatabaseKey As String    'key of the file in the Directory Structure
Public codefield As String      'pft para obter o conteudo abreviado
Public valfield As String       'pft para obter o conteudo completo
Public cfgkey_pft As String     'auxilia a formar a chave a partir de dados do registro de configuracao
Public cfgkey_val As String     'auxilia a formar a chave a partir de dados do form
Public cfgkey_key As String     'auxilia a formar a chave a partir de dados do form


Public level As Long        'nivel no diretorio

'Estes tres elementos formam o nome ou parte do nome do diretorio
Public Prefix As String     'prefixo
Public Value As String      'valor
Public suffix As String     'sufixo


Public IsDatabaseName As String 'Indica se estes tres elementos formam o nome ou parte do nome da base
Public IsDatabaseDir As String 'Indica se estes tres elementos formam o nome ou parte do nome do diretorio da base
Public optional_level As String
'key do label para mensagem de erro
Public MsgInvalidData As String

Public Database As ClIsisDll


Private Sub Class_Initialize()
    Set CfgKeys = New ColPair
    Set ContentListAbbr = New ColPair
    Set ContentListFull = New ColPair
    Set Database = New ClIsisDll
End Sub

Private Sub Class_Terminate()
    Set CfgKeys = Nothing
    Set ContentListAbbr = Nothing
    Set ContentListFull = Nothing
    Set Database = Nothing
End Sub
