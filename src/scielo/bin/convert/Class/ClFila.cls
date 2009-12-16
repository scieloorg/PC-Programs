VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClFila"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private Fila As MyCollection

Public Property Get Primeiro(elem) As Boolean
    Dim ret As Boolean
    
    If Count > 0 Then
        If IsObject(Fila(1)) Then
            Set elem = Fila(1)
        Else
            elem = Fila(1)
        End If
        ret = True
    End If
    Primeiro = ret
End Property

Public Property Get Count() As Long

    Count = Fila.Count
End Property

Public Function Remove(elem As Variant) As Boolean
    If Count > 0 Then
        If IsObject(Fila(1)) Then
            Set elem = Fila(1)
        Else
            elem = Fila(1)
        End If
        Remove = Fila.Remove(1)
    End If
End Function

Public Function Insere(elem As Variant) As Boolean
    Fila.Add (elem)
    Insere = True
End Function

Private Sub Class_Initialize()
    Set Fila = New MyCollection
End Sub

Private Sub Class_Terminate()
    Set Fila = Nothing
End Sub
