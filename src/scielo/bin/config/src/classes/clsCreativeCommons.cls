VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "clsCreativeCommons"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private cc As New ColTextByLang

Sub add(text As String, lang As String)
    Dim textByLang As New ClsTextByLang

    textByLang.lang = lang
    textByLang.text = text
    Call cc.add(textByLang)
End Sub

Function getLicense(lang As String) As ClsTextByLang
    Set getLicense = cc.getItemByLang(lang)
End Function
Function getLicenseByIndex(i As Long) As ClsTextByLang
    Set getLicenseByIndex = cc.getItemByIndex(i)
End Function

Function count() As Long
    count = cc.count
End Function
