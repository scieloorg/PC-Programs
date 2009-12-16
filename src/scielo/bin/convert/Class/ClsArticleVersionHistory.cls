VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsArticleVersionHistory"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private mvarAHPDate As String
Private mvarRVPDate As String
Private mvarAHP_PID As String
Private mvarRVP_PID As String

Public Property Get RVP_PID() As String
    RVP_PID = mvarRVP_PID
End Property

Public Property Let RVP_PID(ByVal vNewValue As String)
    mvarRVP_PID = vNewValue
End Property

Public Property Get AHP_PID() As String
    AHP_PID = mvarAHP_PID
End Property

Public Property Let AHP_PID(ByVal vNewValue As String)
    mvarAHP_PID = vNewValue
End Property
Public Property Get RVPDate() As String
    RVPDate = mvarRVPDate
End Property

Public Property Let RVPDate(ByVal vNewValue As String)
    mvarRVPDate = vNewValue
End Property

Public Property Get AHPDate() As String
    AHPDate = mvarAHPDate
End Property

Public Property Let AHPDate(ByVal vNewValue As String)
    mvarAHPDate = vNewValue
End Property
