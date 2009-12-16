VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClHTMLNode"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private mvarTagInitial As String
Private mvarTagEnd As String
Private mvarText As String
Private mvarCleanedText As String
Private mvarReferenceIndex As String
Private mvarMiddle As New ClHTMLNodes
Private mvarFormerText As String
Public Property Get FormerText() As Variant
    FormerText = mvarFormerText
End Property

Public Property Let FormerText(ByVal vNewValue As Variant)
    mvarFormerText = FormerText
End Property

Public Property Get Middle() As Variant
    Set Middle = mvarMiddle
End Property

Public Property Set Middle(ByVal vNewValue As Variant)
    Set mvarMiddle = Middle
End Property

Public Property Get CleanedText() As Variant
    CleanedText = mvarCleanedText
End Property

Public Property Let CleanedText(ByVal vNewValue As Variant)
    mvarCleanedText = CleanedText
End Property
Public Property Get Text() As Variant
    Text = mvarText
End Property

Public Property Let Text(ByVal vNewValue As Variant)
    mvarText = Text
End Property
Public Property Get ReferenceIndex() As Variant
    ReferenceIndex = mvarReferenceIndex
End Property

Public Property Let ReferenceIndex(ByVal vNewValue As Variant)
    mvarReferenceIndex = ReferenceIndex
End Property

Public Property Get tagEnd() As Variant
    tagEnd = mvarTagEnd
End Property

Public Property Let tagEnd(ByVal vNewValue As Variant)
    mvarTagEnd = tagEnd
End Property

Public Property Get tagInitial() As Variant
    tagInitial = mvarTagInitial
End Property

Public Property Let tagInitial(ByVal vNewValue As Variant)
    mvarTagInitial = tagInitial
End Property

Function getText() As String
    Dim r As String
    
    If mvarMiddle Is Nothing Then
        r = Text
    Else
        r = mvarMiddle.getText()
    End If
    getText = r
End Function

