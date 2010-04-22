VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "clsCodeDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private isis As ClIsisDll

Sub setDB(Path As String, File As String, label As String)
    Set isis = New ClIsisDll
    If isis.Inicia(Path, File, label) Then
        isis.IfCreate (File)
    End If
End Sub
Function getTablesName(filtered As Boolean) As ClsTextCollection
    Dim i As Long
    Dim r As ClsTextCollection
    Dim t As clsText
    Dim name As String
    
    
    Set r = New ClsTextCollection
    
    For i = 1 To isis.MfnQuantity
        name = isis.UsePft(i, "v1^*")
        If ((isis.UsePft(i, "v3") = "1") And filtered) Or (Not filtered) Then
            Set t = r.Item(name)
            If t Is Nothing Then
                Set t = New clsText
                t.text = name
                Call r.Add(t, t.text)
            End If
        End If
    Next
    Set getTablesName = r
End Function
Function getCodes(label As String) As clsTable
    Dim i As Long
    Dim q As Long
    Dim Mfns() As Long
    Dim l As String
    
    Dim res As New clsTable
    Dim code As clsCode
    Dim translation As clsText
    
    Dim codes() As String
    Dim k As Long
    
    res.label = label
    
    q = isis.MfnFind(Replace(label, " ", "_"), Mfns)
    If q > 0 Then
        If (StrComp(label, isis.UsePft(Mfns(q), "v1^*")) = 0) Then
            l = isis.UsePft(Mfns(q), "v1^l")
            res.status = isis.UsePft(Mfns(q), "v3")
            If l = "" Then
                l = "nolang"
            End If
            Set res.code_translations = New clsCodeCollection
            
            For i = 1 To q
                codes = Split(isis.UsePft(Mfns(i), "(v2^c,'%',v2^v,'%')"), "%")
                l = isis.UsePft(Mfns(i), "v1^l")
                
                For k = 0 To UBound(codes) - 1 Step 2
                    
                    Set code = res.code_translations.Item(codes(k))
                    Set translation = New clsText
                    translation.text = codes(k + 1)
                    translation.lang = l
                    If code Is Nothing Then
                        Set code = New clsCode
                        code.code = codes(k)
                        Call res.code_translations.Add(code, codes(k))
                        Set code.translations = New ClsTextCollection
                    End If
                    
                    Call code.translations.Add(translation, l)
                    
                    
                Next
            Next
        End If
    End If
    
    Set getCodes = res
End Function

Sub save(table As clsTable)
    Dim indexLang As Long
    Dim indexCode As Long
    
    Dim q As Long
    Dim Mfns() As Long
    Dim Mfn As Long
    
    Dim id As String
    Dim l As String
    Dim rec As String
    Dim lang As String
    
    
    If table Is Nothing Then
    
    Else
        If table.code_translations Is Nothing Then
        Else
            For indexLang = 1 To table.code_translations.Item(1).translations.Count
                l = ""
                
                If table.code_translations.Item(1).translations(indexLang).lang <> "nolang" Then
                    lang = table.code_translations.Item(1).translations(indexLang).lang
                    l = "^l" + lang
                    
                End If
                rec = "<1>" + table.label + l + "</1>"
                rec = rec + "<3>" + table.status + "</3>"
                
                
                For indexCode = 1 To table.code_translations.Count
                
                    With table.code_translations.Item(indexCode)
                        rec = rec + "<2>^c" + .code + "^v" + .translations.Item(indexLang).text + "</2>"
                    
                    End With
                Next
                
                
                id = table.label
                If Len(lang) > 0 Then id = lang + "_" + id
                id = Replace(id, " ", "_")
                q = isis.MfnFind(id, Mfns)
                
                If q > 0 Then
                    If isis.RecordUpdate(Mfns(q), rec) Then
                        Call isis.IfUpdate(Mfns(q), Mfns(q))
                    End If
                Else
                    Mfn = isis.RecordSave(rec)
                    If Mfn > 0 Then Call isis.IfUpdate(Mfn, Mfn)
                End If
                
        
            Next
        End If
    End If
End Sub

Function getCodesAndValues(attr As String, Optional lang As String) As String
    Dim q As Long
    Dim Mfns() As Long
    Dim res As String
    Dim find As String
    find = attr
    If Len(lang) > 0 Then find = lang + "_" + find
    find = Replace(find, " ", "_")
    q = isis.MfnFind(find, Mfns)
    If q > 0 Then
        res = res + isis.UsePft(Mfns(q), "(v2^v+|;|)") + vbCrLf
        res = res + isis.UsePft(Mfns(q), "(v2^c+|;|)") + vbCrLf
    Else
        res = res + vbCrLf
        res = res + vbCrLf
    End If
    getCodesAndValues = res
End Function

