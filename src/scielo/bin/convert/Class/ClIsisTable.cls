VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClIsisTable"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Private mVarMst As String
Private mVarFst As String
Private mVarIf As String
Property Let propertyMst(v As String)
    mVarMst = v
End Property
Property Let propertyFst(v As String)
    mVarFst = v
End Property
Property Let propertyIf(v As String)
    mVarIf = v
End Property
Property Get propertyMst() As String
    propertyMst = mVarMst
End Property
Property Get propertyFst() As String
    propertyFst = mVarFst
End Property
Property Get propertyIf() As String
    propertyIf = mVarIf
End Property

Function setDBData(ByRef H As Long) As Boolean
    Call IsisSpaMf(H, mVarMst)
    Call IsisSpaFst(H, mVarFst)
    Call IsisSpaIf(H, mVarIf)
    setDBData = True
End Function


