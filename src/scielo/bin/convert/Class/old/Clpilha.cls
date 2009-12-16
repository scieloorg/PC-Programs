VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClPilha"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private i As Long
Private Item() As Variant

Function Desempilha(Elem) As Boolean
    Dim ret As Boolean
    
    If i > 0 Then
        Elem = Item(i)
        i = i - 1
        ReDim Preserve Item(i)
        ret = True
    End If
    Desempilha = ret
End Function

Sub Empilha(Elem)
    i = i + 1
    ReDim Preserve Item(i)
    Item(i) = Elem
End Sub

Sub Inicia()
    
End Sub

Property Get Topo(Elem) As Boolean
    Dim ret As Boolean
    If i > 0 Then
        Elem = Item(i)
        ret = True
    End If
    Topo = ret
End Property
Function Vazia() As Boolean
    Vazia = (i = 0)
End Function

Private Sub Class_Initialize()
    i = 0
End Sub


