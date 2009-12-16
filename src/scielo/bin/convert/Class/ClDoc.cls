VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClDoc"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Const SEM_HTML = "0"
Const PARCIAL_HTML = "1"
Const COM_HTML = "2"

Public ParagCounter As Long

Private mvarRegistro As ClIsisDll 'local copy
Private mvarRegistros As ColRegistro  'local copy
Private RegLinkados As ColLink
Private TodosReg As ColRegistro
Private ColReg As New Collection
Private mvarReferences() As String 'local copy
Private mvarReferencesCounter As Long 'local copy


Public Property Let ReferencesCounter(ByVal vData As Long)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.ReferencesCounter = 5
    ReDim Preserve mvarReferences(vData)
    mvarReferencesCounter = vData
End Property


Public Property Get ReferencesCounter() As Long
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.ReferencesCounter
    ReferencesCounter = mvarReferencesCounter
End Property

Public Property Let References(i As Long, ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.References = 5
    If i > ReferencesCounter Then ReferencesCounter = i
        
    mvarReferences(i) = vData
End Property

Public Property Get References(i As Long) As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.References
    If i <= ReferencesCounter Then References = mvarReferences(i)
End Property

Public Property Set registro(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.Registro = Form1
    Set mvarRegistro = vData
End Property

Public Property Get registro() As ClIsisDll
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: ''Debug.Print X.Records
    Set registro = mvarRegistro
End Property

Public Property Set Records(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.Records = Form1
    Set mvarRegistros = vData
End Property

Public Property Get Records() As ColRegistro
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: ''Debug.Print X.Records
    Set Records = mvarRegistros
End Property

'-----------------------------------------------------------------------
'SortRecords - prepara para gravar um documento na base de dados
'PathDocumento  - caminho do documento
'NomeDocumento  - nome do arquivo do documento
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function SortRecords(PathDocumento As String, NomeDocumento As String, pii As String) As Boolean
    Dim Reunido As ClRegistro
    Dim Item As ClRegistro
    Dim Reunidos As ColRegistro
    Dim i As Long
    Dim Indice As Long
    Dim existe As Boolean
    Dim Info As String
    Dim IdxTpReg As Long
    
    Info = Info + TagContents(pii, ISISTAGS("pii").value) + TagContents(PathDocumento + PathSep + NomeDocumento, ISISTAGS("docfile").value)
    Info = Info + TagContents(GlVar("literattp").value, ISISTAGS("literattp").value)
        

        'Agrupar/classificar/montar os Records
        Set Reunidos = New ColRegistro
        Set Reunido = Reunidos.Add(RecordInfo(1).label + "1")
        Reunido.conteudo = TagContents(GetDateISO(Date), ISISTAGS("update").value)
        
        'Montar os Records
        For i = 1 To Records.count
            With Records(i)
            Set Reunido = Reunidos(.Tipo + .Id, existe)
            If Not existe Then Set Reunido = Reunidos.Add(.Tipo + .Id)
            
            Reunido.conteudo = Reunido.conteudo + TagContents(.conteudo, .Campo)
            End With
        Next
        Set Item = Reunidos(RecordInfo(1).label + "1")
        'Item.conteudo = Item.conteudo + TagContents(CStr(Reunidos.Count), ISISTAGS("reccount").value)
        
        'Conteudo que ocorre em mais de um registro
        'For i = 1 To TodosReg.count
            'With TodosReg(i)
            'Indice = 1
            'Set Reunido = Reunidos(.Tipo + CStr(Indice), existe)
            'While existe
                'Altera Value de pii para todos os Records
                'If (.Campo = ISISTAGS("pii").value) Then .conteudo = pii
                
                'Reunido.conteudo = TagContents(.conteudo, .Campo) + Reunido.conteudo
                'Indice = Indice + 1
                'Set Reunido = Reunidos(.Tipo + CStr(Indice), existe)
            'Wend
            'End With
        'Next
        
        'Ordena os Records
        Set Records = Nothing
        Set Records = New ColRegistro
        
        For i = 1 To RecordInfo.count
            RecordInfo(i).index = 0
        Next
        
        For i = 1 To RecordInfo.count
            IdxTpReg = 0
            Indice = 1
            
            Set Reunido = Reunidos.Item(RecordInfo(i).label + CStr(Indice), existe)
            If existe Then
                RecordInfo(i).index = Records.count + 1
            End If
            While existe
                IdxTpReg = IdxTpReg + 1
                Set Item = Records.Add(RecordInfo(i).label + CStr(Indice))
                Item.conteudo = Info + TagContents(RecordInfo(i).label, ISISTAGS("rectp").value) + TagContents(CStr(Records.count), ISISTAGS("recid").value) + TagContents(CStr(IdxTpReg), ISISTAGS("rectpid").value) + Reunido.conteudo
                
                Indice = Indice + 1
                Set Reunido = Reunidos.Item(RecordInfo(i).label + CStr(Indice), existe)
            Wend
        Next
    
    SortRecords = (Records.count > 0)
End Function


Private Function GetParam(ByVal sentence As String, Subcampo As String) As String
    Dim content As String
    Dim P2 As Long
    Dim P1 As Long
    
    sentence = sentence + "^"
    
    P1 = InStr(1, sentence, Subcampo, vbBinaryCompare)
    If P1 > 0 Then
        P2 = InStr(P1 + 1, sentence, "^", vbBinaryCompare)
        If P2 > 0 Then
            content = Mid(sentence, P1 + Len(Subcampo), P2 - P1 - Len(Subcampo))
        End If
    End If
    
    GetParam = content
End Function

'-----------------------------------------------------------------------
'Parser2DBDOC    - aplica os procedimentos na base gerada pelo parser
'-----------------------------------------------------------------------
Function Parser2DBDOC(pii As String) As Boolean
    Dim mfn As Long
    Dim pft As String
    Dim procs() As String
    
    Dim i As Long
    
    Dim paramcount As Long
    Dim param() As String
    
    Dim procedure As String
    Dim content As String
    Dim scope As String
    Dim Subf As String
    
    Dim reg As New ClRegistro
    Dim existe As Boolean
    Dim Indice As Long
    Dim TmpPath As String
    Dim TmpFile As String
    Dim Contents() As String
    Dim ret As Boolean
    Dim j As Long
    Dim LinkedContent As String
    
    Dim type4 As String
    Dim type4count As Long
    Dim type4p1 As Long
    Dim type4p2 As Long
    
    Set Records = New ColRegistro
    Set RegLinkados = New ColLink
    Set TodosReg = New ColRegistro
    
    ret = True
    
    ReDim procs(4)
    procs(1) = "@c:\SciELO\serial\table\artstep1.pro"
    procs(2) = "@c:\SciELO\serial\table\artstep2.pro"
    procs(3) = "@c:\SciELO\serial\table\artstep3.pro"
    procs(4) = "@c:\SciELO\serial\table\art_end.pro"

    Msg.GiveRunInformation ("Procs")
    For mfn = 1 To registro.MfnQuantity
    
        pft = registro.UsePft(mfn, "@c:\SciELO\serial\table\article.pro")
        If Len(pft) > 0 Then
            Call registro.UseProc(mfn, pft)
        End If
    
        'For i = 1 To 4
        '    pft = registro.UsePft(mfn, procs(i))
        '    If Len(pft) > 0 Then
        '        Call registro.UseProc(mfn, pft)
        '    End If
        'Next
        
        content = registro.UsePft(mfn, "v900")
        content = ReplaceString(content, "^", "&#094;")
        
        scope = registro.UsePft(mfn, "v901")
        Subf = registro.UsePft(mfn, "v903")
        
        paramcount = registro.FieldContentAllGet(mfn, 911, param)
        
        For i = 1 To paramcount
            procedure = GetParam(param(i), "^p")
            
            Select Case procedure
            Case "1"
                Call Execute(content, CLng(GetParam(param(i), "^a")), Subf, GetParam(param(i), "^g"), GetParam(param(i), "^r"), GetParam(param(i), "^i"), GetParam(param(i), "^f"), scope, GetParam(param(i), "^k"), GetParam(param(i), "^l"))
        
            Case "2"
                'If GetParam(param(i), "^r") = "c" Then
                    ReferencesCounter = CLng(GetParam(param(i), "^i"))
                    References(ReferencesCounter) = References(ReferencesCounter) + content
                'End If
            Case "3"
                If StrComp(content, "nd", vbTextCompare) <> 0 Then
                    pii = content
                Else
                    pii = ""
                End If
            Case "4"
                content = content + " "
                type4p1 = 1
                type4p2 = InStr(type4p1, content, " ")
                type4count = 0
                While type4p2 > 0
                    type4count = type4count + 1
                    type4 = Mid(content, type4p1, type4p2 - type4p1)
                    Call Execute(type4, CLng(GetParam(param(i), "^a")), Subf, GetParam(param(i), "^g"), GetParam(param(i), "^r"), GetParam(param(i), "^i"), GetParam(param(i), "^f"), scope, GetParam(param(i), "^k") + CStr(type4count), GetParam(param(i), "^l"))
                    type4p1 = type4p2 + 1
                    type4p2 = InStr(type4p1, content, " ")
                Wend
            End Select
        Next
    Next
    Msg.GiveRunInformation ("Fim Procs")
    
    TmpPath = registro.BDPath
    TmpFile = registro.BDNome
    Set registro = Nothing
    DelFile TmpPath, TmpFile + ".*"
    
    For i = 1 To RegLinkados.count
        
        Set reg = Records.Item(RegLinkados.Item(i).Id, existe)
                
        If existe Then
            LinkedContent = reg.conteudo
            For j = 1 To RegLinkados.Item(i).RIdCount
                Set reg = Records.Item(RegLinkados.Item(i).RId(j), existe)
                If existe Then
                    reg.conteudo = LinkedContent + reg.conteudo
                Else
                    Msg.GiveRunInformation ("Linked record: " + RegLinkados.Item(i).RId(j) + " nao existe")
                End If
            Next
            Records.Remove (RegLinkados.Item(i).Id)
        Else
            Msg.GiveRunInformation ("Linked record: " + RegLinkados.Item(i).Id + " nao existe")
        End If
        
    Next
    Set RegLinkados = Nothing
    Parser2DBDOC = ret
End Function

Private Sub Execute(content As String, Field As Long, SubField As String, GrpIdx As String, RecType As String, RecIdx As String, format As Long, scope As String, Key1 As String, Key2 As String)
    Dim p As Long
    Dim FormatedContent As String
    Dim reg As New ClRegistro
    Dim existe As Boolean
    Dim RegLink As New ClLink
    Dim Item As ClRegistro
    
    
    If Len(GrpIdx) > 0 Then GrpIdx = "^i" + GrpIdx

    If Len(Key2) = 0 Then
        Set reg = Records.Item(Key1, existe)
        If Not existe Then Set reg = Records.Add(Key1, Field)
                
        Select Case format
        Case SEM_HTML
            FormatedContent = RmPartialHTML(content, False)
        Case PARCIAL_HTML
            FormatedContent = RmPartialHTML(content, True)
        Case Else
            FormatedContent = content
        End Select
                
        reg.Tipo = RecType
        reg.Id = RecIdx
        reg.Contexto = scope
                
        If Len(SubField) = 0 Then
            reg.conteudo = FormatedContent + reg.conteudo + GrpIdx
        Else
            If SubField Like "[a-z1]" Then
                reg.conteudo = reg.conteudo + "^" + SubField + FormatedContent + GrpIdx
            ElseIf InStr(SubField, "10|11|28|16|17|29") > 0 Then
                reg.conteudo = reg.conteudo + SubField
            Else
                p = InStr(reg.conteudo, "^")
                If p > 0 Then
                    reg.conteudo = Mid(reg.conteudo, 1, p - 1) + SubField + FormatedContent + Mid(reg.conteudo, p) + GrpIdx
                Else
                    reg.conteudo = reg.conteudo + SubField + FormatedContent + GrpIdx
                End If
            End If
        End If
    Else
        Set RegLink = RegLinkados.Item(Key1, existe)
        If existe Then
            RegLink.RIdCount = RegLink.RIdCount + 1
            RegLink.RId(RegLink.RIdCount) = Key2
        Else
            Set RegLink = RegLinkados.Add(Key1)
            RegLink.Id = Key2
        End If
    End If
End Sub

