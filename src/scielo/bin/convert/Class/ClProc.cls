VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClProc"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Public key As String
Public sgmltag As String
Public is_attribute As Boolean

Public LINKBY_FATHER As String
Public LINKBY_INDEX As String
Public LINKBY_CROSSREFERENCE As String
Public LINKBY_FATHER2 As String

Public params As ColParam

Private Sub Class_Initialize()
    Set params = New ColParam
End Sub

Private Sub Class_Terminate()
    Set params = Nothing
End Sub
