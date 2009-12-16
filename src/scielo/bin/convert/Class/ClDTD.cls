VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClDTD"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public name As String 'local copy
Public Version As String 'local copy
Public SGMLDecl As String
Public filename As String 'local copy
Public CTableFile As String 'local copy
Public TranslFile As String
Public ProcFile As String
Public CitationFile As String
Public RecCode As String
Public RecLabel As String
Public LiteratureType As String
Public UnclosedTags As ColPair

Public isLoaded As Boolean

'----------------------------------------------------------------------------------
' This part below was ModProc
'------------------------------------------
Private Procedures As ColProc
Private Translate As ColTrans
Private STANDARD As ColPair


Const tag_key = 1
Const tag_sgmltag = 2
Const tag_isattrib = 3
Const tag_LINKBY_FATHER = 4
Const tag_LINKBY_INDEX = 5
Const tag_LINKBY_CROSSREFERENCE = 6
Const tag_LINKBY_FATHER2 = 7
Const tag_procedure = 8
Const tag_checkdigit = 9


Const subf_proc = "p"
Const subf_content = "c"
Const subf_record = "r"
Const subf_recindex = "i"
Const subf_field = "f"
Const subf_subf = "s"
Const subf_preffix = "z"
Const subf_format = "h"


Sub ReadProcParam(htmlfragpath As String)
    Dim fn As Long
    Dim rectype As String
    Dim tagcitation As String
    Dim tagstandard As String
    Dim exist As Boolean
    Dim model As String
    Dim curritem As ClPair
    Dim CurrStandard As ClPair
    
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
    Dim checkdigit As String
    
    Set Procedures = New ColProc
    Set proc = New ClProc
    Set param = New ClParam
    Set Translate = New ColTrans
    Set transl = New ClTransl
    Set STANDARD = New ColPair
    Set models_db = New ClIsisDll
    Set curritem = New ClPair
    Set CurrStandard = New ClPair
    
    isLoaded = True
    fn = FreeFile
        
    If Len(CitationFile) > 0 Then
        Open htmlfragpath + PathSep + CitationFile For Input As fn
        While Not EOF(fn)
            
            
            Input #fn, rectype, tagcitation, tagstandard
            
            Set CurrStandard = STANDARD.Item(rectype, exist) ' + tagcitation)
            If Not exist Then
                Set CurrStandard = STANDARD.Add(rectype)
            End If
            Set curritem = CurrStandard.Pointer.Add(tagcitation)
            curritem.elem1 = " " + tagcitation
            curritem.elem2 = " " + tagstandard
        Wend
        Close fn
    Else
    End If
    
    Set CurrStandard = Nothing
    Set curritem = Nothing
    
    With models_db
    
    
    If .Initiate(htmlfragpath, ProcFile, "models database") Then
    For Mfn = 1 To .MfnQuantity
            
            key = .FieldContentAllOccGet(Mfn, tag_key, 1)
            sgmltag = .FieldContentAllOccGet(Mfn, tag_sgmltag, 1)
            checkdigit = .FieldContentAllOccGet(Mfn, tag_checkdigit, 1)
            
            
            Set proc = Procedures.Add(key + sgmltag + checkdigit)
            proc.key = key + sgmltag + checkdigit
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
                .content = GetParamProcfromDB(procedure(i), subf_content)
                .record = GetParamProcfromDB(procedure(i), subf_record)
                .recindex = GetParamProcfromDB(procedure(i), subf_recindex)
                .Field = GetParamProcfromDB(procedure(i), subf_field)
                .Subf = GetParamProcfromDB(procedure(i), subf_subf)
                .subf_preffix = GetParamProcfromDB(procedure(i), subf_preffix)
                .format = GetParamProcfromDB(procedure(i), subf_format)
                End With
            Next
        Next
        
    End If
    End With
    Set models_db = Nothing
    'Procedures.CreateMstModels ("models")
    
    fn = FreeFile
    Open htmlfragpath + PathSep + TranslFile For Input As fn
    While Not EOF(fn)
        Input #fn, key, model
        Set transl = Translate.Add(key)
        transl.Field = key
        transl.model = model
    Wend
    Close fn
End Sub

Private Function GETRECINDEX(scope As String, rectype As String, scope_index As String) As Boolean
    '----------------------------------------------------
    ' GETRECINDEX
    ' Se k = "" e' porque scope nao e' de referencia.
    '---------------------------------------------------
    
    Dim i As Long
    Dim j As Long
    Dim recordfound As Boolean
    Dim found As Boolean
    Dim P As Long
    Dim p2 As Long
    Dim k As String
    Dim curritem As ColPair
    Dim CurrStandard As ClPair
    
    Set curritem = New ColPair
    Set CurrStandard = New ClPair
    
            
    If Len(CitationFile) > 0 Then
        Set CurrStandard = STANDARD.Item(rectype, recordfound) ' + tagcitation)
        If recordfound Then
            found = False
            Set curritem = CurrStandard.Pointer
            While (Not found) And (i < CurrStandard.Pointer.Count)
                i = i + 1
                With CurrStandard.Pointer(i)
                P = InStr(scope, .elem1)
                p2 = InStr(scope, .elem2)
                If (P > 0) And (p2 > 0) Then
                    found = True
                    P = P + Len(.elem1) + 1
                    k = Mid(scope, P, p2 - P)
                End If
                End With
            Wend
        Else
            found = False
            While (Not found) And (i < STANDARD.Count)
                i = i + 1
                j = 0
                With STANDARD(i)
                While (Not found) And (j < .Pointer.Count)
                    j = j + 1
                    With .Pointer(j)
                    P = InStr(scope, .elem1)
                    p2 = InStr(scope, .elem2)
                    If (P > 0) And (p2 > 0) Then
                        found = True
                        P = P + Len(.elem1) + 1
                        k = Mid(scope, P, p2 - P)
                    End If
                    End With
                Wend
                End With
            Wend
        End If
    End If
    scope_index = k
    
    GETRECINDEX = recordfound
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
                                ByVal check_sgmltag As String, _
                                ByVal scope As String, _
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
    Set transl = Nothing
    
    'It looks the procedure identified by the <model> and by the <sgmltag>,
    'if it is necessary
    Set proc = New ClProc
    
    Set proc = Procedures.Item(model + sgmltag + check_sgmltag, exist)
    If exist Then
        model = model + sgmltag + check_sgmltag
    Else
        Set proc = Procedures.Item(model + sgmltag, exist)
        If exist Then
            model = model + sgmltag
        Else
            Set proc = Procedures.Item(model, exist)
        End If
    End If
    
    
    If exist Then
        'get ContentFatherScope, FieldIndex, CrossReference
        Call GetContext(scope, proc, ContentFatherScope, FieldIndex, CROSSREFERENCE)
        
        'insert the <FieldIndex> in subfield
        If Len(FieldIndex) > 0 Then FieldIndex = "^i" + FieldIndex
        
    Else

        'If the procedure not found, create a file to list the not found models.
        Dim fn As Long
        fn = 2
        Open "nomodel.txt" For Append As fn
        Print #fn, model_key
        Close fn
    End If

    Set ReturnProcedure = proc
End Function

'-----------------------------------------------------------------------
'GetProcParam   - Get procedure type and parameters
'proc       - procedures
'paramidx    - procedure index
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
Public Function GetProcParam(ByVal param As ClParam, _
                             ByVal model_key As String, _
                                ByVal content As String, _
                                ByVal scope As String, _
                                ByVal ContentFatherScope As String, _
                                ByVal CROSSREFERENCE As String, _
                                record As String, _
                                recindex As String, _
                                rfield As String, _
                                Subf As String, _
                                subf_preffix As String, _
                                format As String, _
                                fieldkey As String, _
                                LinkKey As String, _
                                rcontent As String) As String
                                
    Dim isValidProcedure As Boolean
    Dim proctype As String
    Dim scope_recidx As String
    Dim recordfound As Boolean

    With param

    'get the record index
    recordfound = GETRECINDEX(scope, .record, scope_recidx)
    If .recindex = "*" Then
        isValidProcedure = True
    ElseIf recordfound And (Len(scope_recidx) > 0) And (.recindex = "?") Then
        isValidProcedure = True
    ElseIf (Not recordfound) And (Len(scope_recidx) = 0) And (.recindex <> "?") Then
        isValidProcedure = True
    End If
            
    Debug.Print scope, .record, recordfound, isValidProcedure
    If isValidProcedure Then
        'it is a valid procedure then continue to get its parameters

        proctype = .proc
        record = .record
        
        recindex = scope_recidx
        If .recindex <> "?" Then recindex = .recindex
                
        format = .format
                
        If Len(.Field) = 0 Then
            rfield = model_key
        Else
            rfield = .Field
        End If
                
        If Len(CROSSREFERENCE) = 0 Then
            fieldkey = rfield + .record + recindex + ContentFatherScope
            LinkKey = ""
        Else
            fieldkey = rfield + .record + recindex + content + ContentFatherScope
            LinkKey = rfield + .record + recindex + CROSSREFERENCE
        End If
        subf_preffix = .subf_preffix
        Subf = .Subf
        rcontent = content
        If Len(.content) > 0 Then
            rcontent = .content
        End If
    Else
        proctype = "0"
    End If
    End With

    GetProcParam = proctype
End Function


Private Function GetParamProcfromDB(procedure As String, Subf As String) As String
    Dim P As Long
    Dim p2 As Long
    Dim param As String
    
    P = InStr(procedure, CONST_SUBFIELDINDICATOR + Subf)
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
    Dim P As String
    
    'byfather = ""
    byfather = scope
    byIndex = ""
    byCROSSREFERENCE = ""
    
    With proc
    If (Len(.LINKBY_FATHER) > 0) Or (Len(.LINKBY_INDEX) > 0) Or (Len(.LINKBY_CROSSREFERENCE) > 0) Or (Len(.LINKBY_FATHER2) > 0) Then
        If Len(.LINKBY_FATHER) > 0 Then
            P = InStr(1, scope, .LINKBY_FATHER, vbTextCompare)
            If P > 0 Then
                FatherScope = Mid(scope, P + Len(.LINKBY_FATHER), Len(scope))
                If InStr(scope, "ign:") = 1 Then
                    FatherScope = ":1" + Mid(FatherScope, InStr(FatherScope, " "))
                End If
            End If
        End If
        
        If Len(.LINKBY_INDEX) > 0 Then
            P = InStr(1, scope, .LINKBY_INDEX, vbTextCompare)
            If P > 0 Then
                byIndex = Mid(scope, P + Len(.LINKBY_INDEX))
                byIndex = Mid(byIndex, 1, InStr(1, byIndex, Chr(32)) - 1)
            End If
        End If
        If Len(.LINKBY_CROSSREFERENCE) > 0 Then
           P = InStr(1, scope, .LINKBY_CROSSREFERENCE, vbTextCompare)
           If P > 0 Then
                'valor para o byCROSSREFERENCE e' o mesmo do fatherscope
                CROSSREFERENCE = Mid(scope, P)
                byCROSSREFERENCE = FatherScope
            End If
        End If
        If Len(.LINKBY_FATHER2) > 0 Then
            'byfather = .LINKBY_FATHER2 + scope
            FatherScope = .LINKBY_FATHER2 + " " + scope
        End If
        
        If Len(CROSSREFERENCE) > 0 Then
            byfather = CROSSREFERENCE
        Else
            byfather = FatherScope
        End If
    Else
        byfather = scope
    End If
    End With
End Sub

Private Sub Class_Initialize()
    Set UnclosedTags = New ColPair
End Sub

Private Sub Class_Terminate()
    Set UnclosedTags = Nothing
End Sub

Sub SetUnclosedTags(Tags As String)
    Dim q As Long
    Dim Tag() As String
    Dim i As Long
    Dim it As ClPair
    
    q = GetElemStr(Tags, ",", Tag)
    
    Set UnclosedTags = New ColPair
    Set it = New ClPair
    For i = 1 To q
        Set it = UnclosedTags.Add(Tag(i))
        it.elem1 = Tag(i)
    Next
    Set it = Nothing
End Sub

'Function GetUnclosedTags(index As Long) As String
'    Dim tag As String
'
'    If index > 0 And index <= UnclosedTags.Count Then
'        tag = UnclosedTags(index).elem1
'    End If
'    GetUnclosedTags = tag
'End Function
'
'Function GetUnclosedTagsCount() As Long
'    GetUnclosedTagsCount = UnclosedTags.Count
'End Function
