VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsCodesDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private isis As ClIsisdll

Sub create(Path As String, FileName As String, key As String)
    Set isis = New ClIsisdll
    If isis.Inicia(Path, FileName, key) Then
        If isis.IfCreate(FileName) Then
        
        End If
    End If
End Sub

Sub getTable(idiom As String, key As String, Code As ColCode, Optional codeEqualValue As Boolean = False)
    Dim mfn As Long
    Dim mfns() As Long
    Dim q As Long
    Dim i As Long
    Dim aux As String
    Dim a_codes() As String
    Dim a_values() As String
    Dim a() As String
    Dim itemCode As ClCode
    Dim exist As Boolean
    Dim format As String
    Dim tracing As String
    Dim find As String
    
    Set Code = New ColCode
    
    i = 0
    mfn = 0
    
    find = key
    If Len(idiom) > 0 Then
        find = idiom & "_" & find
    End If
    
    find = Replace(find, " ", "_")
    'q = isis.MfnFind(Replace(find, " ", "_"), mfns)
    q = isis.MfnFind(find, mfns)
    
    format = "if s(v1^*)='" + key + "' and (s(v1^l)='" + idiom + "' or a(v1^l))  then (v2^v|;|),'|',(v2^c|;;|) fi"
    
    If q > 0 Then
        While (i < q) And (mfn = 0)
            i = i + 1
            aux = isis.UsePft(mfns(i), format)
            If Len(aux) > 0 Then mfn = mfns(i)
        Wend
    Else
        q = isis.MfnQuantity
        While (i < q) And (mfn = 0)
            i = i + 1
            aux = isis.UsePft(i, format)
            If Len(aux) > 0 Then mfn = i
        Wend
    End If
    tracing = vbCrLf & "format: " & format & vbCrLf & "result:" & aux & vbCrLf & "mfn: " & CStr(mfn)
    
    If mfn > 0 Then
        a = Split(aux, "|")
        a_values = Split(a(0), ";")
        a_codes = Split(a(1), ";;")
        
        For i = 0 To UBound(a_values) - 1
            Set itemCode = Code.item(CVar(a_codes(i)), exist)
            tracing = tracing + vbCrLf + "(" + a_codes(i) + "," + a_values(i) + ")" + CStr(exist)
            If Not exist Then
                Set itemCode = New ClCode
                
                itemCode.Code = a_codes(i)
                If codeEqualValue Then
                    itemCode.value = a_codes(i)
                Else
                    itemCode.value = a_values(i)
                End If
                Call Code.add(itemCode, CVar(a_codes(i)))
            End If
        Next
        
    End If
    
    If Code.count = 0 Then MsgBox "clsCodeDAO.getTable" + vbCrLf + isis.MSTFULLPATH + vbCrLf + find + " " + tracing
    
    
End Sub

Sub getMultilingueTable(key As String, tableList As ColObjByLang)
    
    Dim mfn As Long
    Dim mfns() As Long
    Dim q As Long
    Dim i As Long
    Dim k As Long
    Dim aux As String
    Dim a_codes() As String
    Dim a_values() As String
    Dim a() As String
    Dim table As ColCode
    Dim itemCode As ClCode
    Dim exist As Boolean
    Dim format As String
    Dim tracing As String
    Dim find As String
    Dim lang As String
    
    
    Set tableList = New ColObjByLang
            
    mfn = 0
    
    
    find = key
    find = Replace(find, " ", "_")
    
    q = isis.MfnFind(find, mfns)
    format = "if s(v1^*)='" + key + "' then (v2^v|§|),'|',(v2^c|§§|) fi,,'|',v1^l"
    For k = 1 To q
        aux = isis.UsePft(mfns(k), format)
        If Len(aux) > 0 Then
            mfn = mfns(k)
            tracing = vbCrLf & "format: " & format & vbCrLf & "result:" & aux & vbCrLf & "mfn: " & CStr(mfn)
            
            If mfn > 0 Then
                a = Split(aux, "|")
                a_values = Split(a(0), "§")
                a_codes = Split(a(1), "§§")
                lang = a(2)
                Set table = New ColCode
                table.lang = lang
                
                For i = 0 To UBound(a_values) - 1
                    Set itemCode = New ClCode
                    itemCode.value = a_values(i)
                    itemCode.Code = a_codes(i)
                    Call table.add(itemCode, CVar(a_codes(i)))
                Next
                
                Call tableList.add(table)
            End If
        End If
    Next
    If tableList.count = 0 Then MsgBox "getMultilingueTable count=0 q=" + CStr(q) + " " + find + " " + tracing
    
    
End Sub
