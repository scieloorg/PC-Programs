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

Private labels As ClsTextCollection

Sub SetLabels(CurrCodeIdiom As String)
    
    Dim fn As Long
    Dim id As String
    Dim val As String
    Dim t As clsText
    Set labels = New ClsTextCollection
    
    fn = FreeFile
    Open CurrCodeIdiom + "_labels.ini" For Input As fn
    While Not EOF(fn)
        Input #fn, id, val
        Set t = New clsText
        t.text = val
        t.id = id
        labels.Add t, t.id
    Wend
    Close fn
    
    
End Sub

Function getLabel(id As String) As String
    getLabel = labels(id).text
End Function
