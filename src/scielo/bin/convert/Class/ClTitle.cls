VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClTitle"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private mVarSciELONet As Collection

Property Get SciELONet(Optional id As String)

End Property

Function setDBData(mst As String, fst As String, iffile As String) As Boolean
    Call IsisSpaMf(mVarH, mst)
    Call IsisSpaFst(mVarH, fst)
    Call IsisSpaIf(mVarH, iffile)
    setDBData = True
End Function

Function getArticleInfo(order As String, ByRef inicio As Long, ByRef fim As Long, ByRef FileName As String) As Boolean

Const MaxSizeArea = 60000

    Dim Mfn As Long
    Dim QtdTrm As Long
    Dim pIsisTrmMfn() As IsisTrmMfn
    Dim pIsisTrmRead As IsisTrmRead
    Dim q As Long
    Dim Occ As Long
    
    Dim area As String * MaxSizeArea
    Dim qtdDocRecords As String
    Dim r As Long
    Dim QtdOcc As Long
    
    pIsisTrmRead.key = order
    QtdTrm = IsisTrmReadMap(mVarH, 0, pIsisTrmRead)
    If QtdTrm > ZERO Then
    
        ReDim pIsisTrmMfn(QtdTrm)
        q = IsisTrmMfnMap(mVarH, 0, 1, QtdTrm, pIsisTrmMfn(0))
        If q > 0 Then
            Mfn = pIsisTrmMfn(0).Mfn
            If Mfn > 1 Then
                inicio = Mfn - 1
                r = IsisRecRead(mVarH, 0, inicio)
                If r = ZERO Then
                    QtdOcc = IsisRecFieldOcc(mVarH, 0, 703)
                    If (QtdOcc > 0) Then
                        area = ""
                        r = IsisRecField(mVarH, 0, 703, 1, area, MaxSizeArea)
                        If r > ZERO Then
                            qtdDocRecords = Left(area, r)
                            If CInt(qtdDocRecords) > 1 Then
                                fim = inicio + qtdDocRecords - 1
                            End If
                        End If
                    End If
                    QtdOcc = IsisRecFieldOcc(mVarH, 0, 2)
                    If (QtdOcc > 0) Then
                        area = ""
                        r = IsisRecField(mVarH, 0, 2, 1, area, MaxSizeArea)
                        If r > ZERO Then
                            FileName = Left(area, r)
                        End If
                    End If
                End If
            End If
        End If
    End If
    getArticleInfo = (inicio < fim) And (inicio > 1) And (FileName <> "")
End Function


Function deleteExAhead(inicio As Long, fim As Long) As Boolean
    Dim ret As Boolean
    Dim Mfn As Long
    
    
    If (inicio > 0) And (fim >= inicio) Then
    For Mfn = inicio To fim
        Call IsisRecShelfSize(mVarH, 0, 3 * MAXMFRL)
        If IsisRecRead(mVarH, 0, Mfn) = ZERO Then
            If IsisRecFieldUpdate(mVarH, 0, "d.") = ZERO Then
                If IsisRecWrite(mVarH, 0) = ZERO Then
                    If IsisRecIfUpdate(mVarH, Mfn) = ZERO Then
                        ret = True
                    End If
                End If
            End If
        End If
    Next
    
    End If
    
    deleteExAhead = ret
End Function

Function getOrder(pid As String) As String
    getOrder = Trim(CStr(CInt(Mid(pid, Len(pid) - 5))))
End Function

