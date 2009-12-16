VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsSections"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private sections As New Collection

Sub add(value As ClsSection, key As String)
    
    
    Call sections.add(value, key)
    
End Sub
Function count() As Long
    count = sections.count
End Function



Function item(index As Variant) As ClsSection
On Error GoTo set_nothing
  Set item = sections.item(index)
  Exit Function
set_nothing:
Set item = Nothing
End Function


