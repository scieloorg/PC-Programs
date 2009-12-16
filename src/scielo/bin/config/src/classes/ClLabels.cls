VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClLabels"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private labels As ClsParams

Function getLabel(key As String) As String
    getLabel = labels.item(key)
End Function

Sub SetLabels(CurrCodeIdiom As String)
    
    Dim fn As Long
    Dim value As String
    Dim key As String
    Set labels = New ClsParams
    
    fn = FreeFile
    Open App.Path + "\langs\" + CurrCodeIdiom + "_labels.ini" For Input As fn
    While Not EOF(fn)
        Input #fn, key, value
        Call labels.add(value, key)
    Wend
    
    FormMenuPrin.SetLabels
End Sub


