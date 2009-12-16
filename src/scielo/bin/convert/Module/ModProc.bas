Attribute VB_Name = "ModProc"
Option Explicit


Private Procedures As ColProc
Private Translate As ColTrans
Private STANDARD As ColPair
Private CurrStandard As ClPair

Const tag_key = 1
Const tag_sgmltag = 2
Const tag_isattrib = 3
Const tag_LINKBY_FATHER = 4
Const tag_LINKBY_INDEX = 5
Const tag_LINKBY_CROSSREFERENCE = 6
Const tag_LINKBY_FATHER2 = 7
Const tag_procedure = 8

Const subf_proc = "p"
Const subf_record = "r"
Const subf_recindex = "i"
Const subf_field = "f"
Const subf_subf = "s"
Const subf_format = "h"


Sub ReadProcParam(TablePath As String, DTD As ClDTD)
    Dim fn As Long
    Dim tagcitation As String
    Dim tagstandard As String
    Dim exist As Boolean
    Dim model As String
    
    Dim proc As ClProc
    Dim transl As ClTransl
    Dim param As ClParam
    
    Dim i As Long
    Dim models_db As ClIsisDll
    Dim procedure() As String
    Dim q As Long
    Dim Mfn As Long
    Dim key As String
    Dim sgmltag As String
    
    Set Procedures = New ColProc
    Set proc = New ClProc
    Set param = New ClParam
    Set Translate = New ColTrans
    Set transl = New ClTransl
    Set STANDARD = New ColPair
    Set models_db = New ClIsisDll
    
    If Len(DTD.CitationFile) > 0 Then
        fn = 1
        Open TablePath + PathSep + DTD.CitationFile For Input As fn
        While Not EOF(fn)
            Input #fn, tagcitation, tagstandard
            Set CurrStandard = STANDARD.Add(tagcitation)
            CurrStandard.elem1 = tagcitation
            CurrStandard.elem2 = tagstandard
        Wend
        Set CurrStandard = Nothing
        Close fn
    Else
        Set CurrStandard = Nothing
    End If
    
    With models_db
    If .Initiate(TablePath, DTD.ProcFile, "models database") Then
        For Mfn = 1 To .MfnQuantity
            
            key = .FieldContentAllOccGet(Mfn, tag_key, 1)
            sgmltag = .FieldContentAllOccGet(Mfn, tag_sgmltag, 1)
            
            Set proc = Procedures.Add(key + sgmltag)
            proc.key = key
            proc.sgmltag = sgmltag
            If .FieldContentAllOccGet(Mfn, tag_isattrib, 1) = "1" Then proc.is_attribute = .FieldContentAllOccGet(Mfn, 3, 1)
            proc.LINKBY_FATHER = .FieldContentAllOccGet(Mfn, tag_LINKBY_FATHER, 1)
            proc.LINKBY_INDEX = .FieldContentAllOccGet(Mfn, tag_LINKBY_INDEX, 1)
            proc.LINKBY_CROSSREFERENCE = .FieldContentAllOccGet(Mfn, tag_LINKBY_CROSSREFERENCE, 1)
            proc.LINKBY_FATHER2 = .FieldContentAllOccGet(Mfn, tag_LINKBY_FATHER2, 1)
                       
            q = .FieldContentAllGet(Mfn, tag_procedure, procedure)
            
            For i = 1 To q
                Set param = proc.params.Add
                With param
                .proc = GetParamProcfromDB(procedure(i), subf_proc)
                .record = GetParamProcfromDB(procedure(i), subf_record)
                .recindex = GetParamProcfromDB(procedure(i), subf_recindex)
                .field = GetParamProcfromDB(procedure(i), subf_field)
                .subf = GetParamProcfromDB(procedure(i), subf_subf)
                .format = GetParamProcfromDB(procedure(i), subf_format)
                End With
            Next
        Next
        
    End If
    End With
    'Procedures.CreateMstModels ("models")
    
    Open TablePath + PathSep + DTD.TranslFile For Input As fn
    While Not EOF(fn)
        Input #fn, key, model
        Set transl = Translate.Add(key)
        transl.field = key
        transl.model = model
    Wend
    Close fn
End Sub

Private Function GETRECINDEX(scope As String) As String
    '----------------------------------------------------
    ' GETRECINDEX
    ' Se k = "" e' porque scope nao e' de referencia.
    '---------------------------------------------------
    
    Dim i As Long
    Dim found As Boolean
    Dim P As Long
    Dim p2 As Long
    Dim k As String
    
        
    If CurrStandard Is Nothing Then
        While (Not found) And (i < STANDARD.Count)
            i = i + 1
            P = InStr(scope, STANDARD.Item(i).elem1)
            p2 = InStr(scope, STANDARD.Item(i).elem2)
            If (P > 0) And (p2 > 0) Then
                Set CurrStandard = STANDARD.Item(i)
                found = True
                P = P + Len(CurrStandard.elem1) + 1
                k = Mid(scope, P, p2 - P - 1)
            End If
        Wend
    Else
        P = InStr(scope, CurrStandard.elem1)
        p2 = InStr(scope, CurrStandard.elem2)
        If (P > 0) And (p2 > 0) Then
            P = P + Len(CurrStandard.elem1) + 1
            k = Mid(scope, P, p2 - P - 1)
        End If
    End If

    GETRECINDEX = k
End Function

'-----------------------------------------------------------------------
'ReturnProcedure   - Return procedure and ...
'model_key    - input, identify the procedure model, it means, it gives the rules to store
'               the content in the database
'sgmltag    - input, sgml tag which tags the content, if it is necessary. It is only necessary
'             when more than one content is stored in the same field
'scope      - input, path of the content on the tree structure
'
'Return the number of procedures and their type and their parameters
'scope_recidx   - record index in scope
'ContentFatherScope   - input, return the 'father scope'. It must be the same for all the contents
'               which will be stored in the same field. It is defined by the conversion tables
'FieldIndex     - identifies which contents are grouped, since they are not stored in the same
'               field, but they are stored in the same record and linked by the <GrpIdx>
'CrossReference - input, return the father scope of the id/CrossReference
'exist  - return <True> if the procedure exists, <False> otherwise
'return     - the procedure
'-----------------------------------------------------------------------
Public Function ReturnProcedure(ByVal model_key As String, _
                                ByVal sgmltag As String, _
                                ByVal scope As String, _
                                scope_recidx As String, _
                                ContentFatherScope As String, _
                                FieldIndex As String, _
                                CROSSREFERENCE As String, _
                                exist As Boolean) As ClProc
                                
    Dim transl As ClTransl
    Dim proc As ClProc
    Dim model As String
    
    'It looks the procedure model in the translation table by <model_key>,
    'if it is not found then the model looked is the proper <model_key>
    Set transl = New ClTransl
    Set transl = Translate.Item(model_key, exist)
    If exist Then
        model = transl.model
    Else
        model = model_key
    End If
            
    'It looks the procedure identified by the <model> and by the <sgmltag>,
    'if it is necessary
    Set proc = New ClProc
    Set proc = Procedures.Item(model, exist)
    If Not exist Then
        Set proc = Procedures.Item(model + sgmltag, exist)
        If exist Then model = model + sgmltag
    End If
    
    If exist Then
        'get ContentFatherScope, FieldIndex, CrossReference
        Call GetContext(scope, proc, ContentFatherScope, FieldIndex, CROSSREFERENCE)
        
        'insert the <FieldIndex> in subfield
        If Len(FieldIndex) > 0 Then FieldIndex = "^i" + FieldIndex
        
        'get the record index
        scope_recidx = GETRECINDEX(scope)
            
    Else
        'If the procedure not found, create a file to list the not found models.
        Dim fn As Long
        fn = 1
        Open "nomodel.txt" For Append As fn
        Print #fn, model_key
        Close fn
    End If
    Set ReturnProcedure = proc
End Function

'-----------------------------------------------------------------------
'GetProcParam   - Get procedure type and parameters
'proc       - procedures
'procidx    - procedure index
'field  - original field
'content    - input, tagged content by <sgmltag>
'scope_recidx   - record index in scope
'ContentFatherScope   - input, return the 'father scope'. It must be the same for all the contents
'               which will be stored in the same field. It is defined by the conversion tables
'CrossReference - input, return the father scope of the id/CrossReference
'
'
'Return the number of procedures and their type and their parameters
'record     - record label
'recindex   - record index
'rfield     - field in database
'subf       - subfield in database, if exists
'format     - type of formatation which the content will be presented/stored
'FieldKey - identify the field
'LinkKey       - identify the field to be linked later
'rcontent   - changed content
'return     - procedure type
'-----------------------------------------------------------------------
Public Function GetProcParam(ByVal proc As ClProc, _
                             ByVal procidx As Long, _
                             ByVal model_key As String, _
                                ByVal content As String, _
                                ByVal scope_recidx As String, _
                                ByVal ContentFatherScope As String, _
                                ByVal CROSSREFERENCE As String, _
                                record As String, _
                                recindex As String, _
                                rfield As String, _
                                subf As String, _
                                format As String, _
                                FieldKey As String, _
                                LinkKey As String, _
                                rcontent As String) As String
                                
    Dim isValidProcedure As Boolean
    Dim proctype As String
        
    With proc.params(procidx)
            
    If (Len(scope_recidx) = 0) Then
        If .recindex <> "?" Then
            isValidProcedure = True
        End If
    Else
        If .recindex = "?" Then
            isValidProcedure = True
        End If
    End If
            
    If isValidProcedure Then
        'it is a valid procedure then continue to get its parameters
                
        proctype = .proc
        record = .record
                
        recindex = scope_recidx
        If .recindex <> "?" Then recindex = .recindex
                
        format = .format
                
        If Len(.field) = 0 Then
            rfield = model_key
        Else
            rfield = .field
        End If
                
        If Len(CROSSREFERENCE) = 0 Then
            FieldKey = rfield + .record + recindex + ContentFatherScope
            LinkKey = ""
        Else
            FieldKey = rfield + .record + recindex + content + ContentFatherScope
            LinkKey = rfield + .record + recindex + CROSSREFERENCE
        End If
            
        If InStr(.subf, "10|11|28|16|17|29") = 0 Then
            subf = .subf
            rcontent = content
        Else
            rcontent = .subf
            subf = ""
        End If
    Else
        proctype = "0"
    End If
    End With
    
    GetProcParam = proctype
End Function


Private Function GetParamProcfromDB(procedure As String, subf As String) As String
    Dim P As Long
    Dim p2 As Long
    Dim param As String
    
    P = InStr(procedure, CONST_SUBFIELDINDICATOR + subf)
    If P > 0 Then
        p2 = InStr(P + 1, procedure, CONST_SUBFIELDINDICATOR, vbBinaryCompare)
        If p2 = 0 Then p2 = Len(procedure) + 1
        param = Mid(procedure, P + 2, p2 - P - 2)
    End If
    GetParamProcfromDB = param
End Function

'-----------------------------------------------------------------------
'GetContext   - Get the byfather, the byIndex and the byCrossReference of the content
'scope      - input, path of the content on the document tree structure
'proc       -
'byfather   - output, return the 'father scope'. It must be the same for all the contents
'               which will be stored in the same field. It is defined by the conversion tables
'byIndex    - output, return the index which will be added as a subfield in all the fields
'               that must be linked by this index
'byCrossReference      - output, return the father scope of the id/CrossReference
'-----------------------------------------------------------------------
Private Sub GetContext(scope As String, proc As ClProc, byfather As String, byIndex As String, byCROSSREFERENCE As String)
    Dim FatherScope As String
    Dim CROSSREFERENCE As String
    
    byfather = ""
    byIndex = ""
    byCROSSREFERENCE = ""
    
    If (Len(proc.LINKBY_FATHER) > 0) Or (Len(proc.LINKBY_INDEX) > 0) Or (Len(proc.LINKBY_CROSSREFERENCE) > 0) Or (Len(proc.LINKBY_FATHER2) > 0) Then
        If Len(proc.LINKBY_FATHER) > 0 Then
            If InStr(1, scope, proc.LINKBY_FATHER, vbTextCompare) > 0 Then
                FatherScope = Mid(scope, InStr(1, scope, proc.LINKBY_FATHER, vbTextCompare) + Len(proc.LINKBY_FATHER), Len(scope))
                Debug.Print "fatherscope=" & FatherScope
            End If
        End If
        
        If Len(proc.LINKBY_INDEX) > 0 Then
            If InStr(1, scope, proc.LINKBY_INDEX, vbTextCompare) > 0 Then
                byIndex = Mid(scope, InStr(1, scope, proc.LINKBY_INDEX, vbTextCompare) + Len(proc.LINKBY_INDEX))
                byIndex = Mid(byIndex, 1, InStr(1, byIndex, Chr(32)) - 1)
            End If
        End If
        If Len(proc.LINKBY_CROSSREFERENCE) > 0 Then
           If InStr(1, scope, proc.LINKBY_CROSSREFERENCE, vbTextCompare) > 0 Then
                'valor para o byCROSSREFERENCE e' o mesmo do fatherscope
                CROSSREFERENCE = Mid(scope, InStr(1, scope, proc.LINKBY_CROSSREFERENCE, vbTextCompare))
                byCROSSREFERENCE = FatherScope
            End If
        End If
        If Len(proc.LINKBY_FATHER2) > 0 Then
            'byfather = proc.LINKBY_FATHER2 + scope
            FatherScope = proc.LINKBY_FATHER2 + " " + scope
        End If
        
        If Len(CROSSREFERENCE) > 0 Then
            byfather = CROSSREFERENCE
        Else
            byfather = FatherScope
        End If
    Else
        byfather = scope
    End If
End Sub


