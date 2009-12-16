VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClTabConv"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private mvarTabIdTpReg As ClTable
Private mvarTabProc As ClTable
Private mvarTabDTD2BD As ClTable
Private mvarTabGrupos As ClTable 'local copy

Const TamMaxIdGrp = 5
Const GrpLinkIndex = "R"    'Ex: Keywords + subkeys
Const GrpLinkSubc = "S"     'Ex: nome, sobrenome, role, etc
Const GrpLinkSubcRepet = "X" 'Ex: nome, sobrenome, role, etc
Const GrpLinkCampo = "C"    'Ex: conferências


Public Property Set TabGrupos(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.TabGrupos = Form1
    Set mvarTabGrupos = vData
End Property


Public Property Get TabGrupos() As ClTable
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.TabGrupos
    Set TabGrupos = mvarTabGrupos
End Property

Public Property Set TabIdTpReg(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.TabIdTpReg = Form1
    Set mvarTabIdTpReg = vData
End Property

Public Property Get TabIdTpReg() As ClTable
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.TabIdTpReg
    Set TabIdTpReg = mvarTabIdTpReg
End Property

Public Property Set TabProc(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.TabProc = Form1
    Set mvarTabProc = vData
End Property

Public Property Get TabProc() As ClTable
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.TabProc
    Set TabProc = mvarTabProc
End Property

Public Property Set tabdtd2bd(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.tabdtd2bd = Form1
    Set mvarTabDTD2BD = vData
End Property

Public Property Get tabdtd2bd() As ClTable
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.tabdtd2bd
    Set tabdtd2bd = mvarTabDTD2BD
End Property

'-----------------------------------------------------------------------
'Inicia - Inicia as tabelas
'Path   - caminho das tabelas
'TabProcFile    - nome do arquivo da tabela  de procedimentos
'TabDTD2BDFile  - nome do arquivo da tabela  de conversão de tags DTD para campos da base de dados
'IdTpRegFile    - nome do arquivo da tabela  de Records repetitivos
'Retorno        - sucesso ou fracasso
'-----------------------------------------------------------------------
Function Inicia(Path As String, TabProcFile As String, TabDTD2BDFile As String, IdTpRegFile As String) As Boolean
    Dim ret As Boolean
    
    Set TabProc = New ClTable
    If TabProc.Read(Path, TabProcFile, "DTDProc", ",", "func,intermedfield,record,field,group,subf") Then
        Set TabIdTpReg = New ClTable
        If TabIdTpReg.Read(Path, IdTpRegFile, "IdTpReg", ",", "record,tag") Then
            Set tabdtd2bd = New ClTable
            If tabdtd2bd.Read(Path, TabDTD2BDFile, "DTDDTD2BD", ";", "intermedfield,dtdtag,escope") Then
                ObtElemComPrin
                ret = True
            End If
        End If
    End If
    Inicia = ret
End Function

'-----------------------------------------------------------------------
'ObtGrupos  - obtém os grupos, separando em grupo subcampo, campo e index
'gsubc      - grupo subcampo
'gcampo     - grupo campo
'gindex     - grupo index
'-----------------------------------------------------------------------
Sub ObtGrupos(grupo As String, gsubc As String, gcampo As String, gindex As String)
    Dim p As Long
    
    gsubc = ""
    gcampo = ""
    gindex = ""
    p = InStr(grupo, GrpLinkCampo)
    If p > 0 Then gcampo = Mid(grupo, p, TamMaxIdGrp)
    
    p = InStr(grupo, GrpLinkSubc)
    If p > 0 Then gsubc = Mid(grupo, p, TamMaxIdGrp)
    
    p = InStr(grupo, GrpLinkIndex)
    If p > 0 Then gindex = Mid(grupo, p, TamMaxIdGrp)
End Sub

'-----------------------------------------------------------------------
'ObtElemComPrin - obtém os elementos comuns para obtenção dos contextos
'-----------------------------------------------------------------------
Sub ObtElemComPrin()
    Dim grupo As String
    Dim gindex As String
    Dim gcampo As String
    Dim gsubc As String
    Dim i As Long
    Dim idx() As Long
    Dim QtdIdx As Long
    
    
    If tabdtd2bd.AddCol("TabDTD2BD", "FieldCommElem,SubfCommElem,IdxCommElem") Then
        Set TabGrupos = New ClTable
        If TabGrupos.Criar("Tabela Grupos", "group,indices,elemcomum") Then
            For i = 1 To TabProc.RowCounter
                grupo = TabProc.Elem(i, "group")
                If Len(grupo) > 0 Then
                    Call ObtGrupos(grupo, gsubc, gcampo, gindex)
                    
                    QtdIdx = tabdtd2bd.Find(TabProc.Elem(i, "intermedfield"), "intermedfield", idx, vbTextCompare)
                    If QtdIdx = 1 Then
                        Call TabGrupoFill(idx(QtdIdx), gsubc, "SubfCommElem")
                        Call TabGrupoFill(idx(QtdIdx), gcampo, "FieldCommElem")
                        Call TabGrupoFill(idx(QtdIdx), gindex, "IdxCommElem")
                    Else
                        MsgBox "problema em ObtElemComPrin."
                    End If
                End If
            Next
        End If
    End If
    ObtElemComum
        
    
End Sub

'-----------------------------------------------------------------------
'TabGrupoFill - agrupa os índices dos elementos na tabela contexto que estão no mesmo grupo
'indice - índice da tabela contexto
'Grupo  - grupo
'-----------------------------------------------------------------------
Sub TabGrupoFill(Indice As Long, grupo As String, nomegrupo As String)
    Dim q As Long
    Dim Result() As Long
    
    If Len(grupo) > 0 Then
        With TabGrupos
        q = .Find(grupo, "group", Result, vbTextCompare)
    
        If q > 0 Then
            .Elem(Result(q), "indices") = .Elem(Result(q), "indices") + "," + CStr(Indice)
            .Elem(Result(q), "elemcomum") = nomegrupo
        Else
            q = .RowCounter + 1
            .Elem(q, "group") = grupo
            .Elem(q, "elemcomum") = nomegrupo
            .Elem(q, "indices") = CStr(Indice)
        End If
        End With
    End If
    
End Sub

'-----------------------------------------------------------------------
'ObtElemComum - obtém os elementos comuns de um dado grupo e os põe na tabela de contexto
'-----------------------------------------------------------------------
Sub ObtElemComum()
    Dim i As Long
    Dim j As Long
    Dim k As Long
    Dim idx() As String
    Dim QtdIdx As Long
    Dim ElemComum As String
    Dim Caminhos() As String
    Dim p As Long
    Dim P1 As Long
    Dim P2 As Long
    Dim achou As Boolean
    Dim aux As String
        
    For i = 1 To TabGrupos.Colunas(1).Counter
        QtdIdx = GetElemStr(TabGrupos.Elem(i, "indices"), ",", idx)
        If QtdIdx > 0 Then
            ReDim Caminhos(QtdIdx)
            aux = tabdtd2bd.Elem(CLng(idx(1)), "escope")
            If Len(aux) > 0 Then aux = aux + ","
            Caminhos(1) = tabdtd2bd.Elem(CLng(idx(1)), "dtdtag") + "," + aux
            
            For j = 2 To QtdIdx
                aux = tabdtd2bd.Elem(CLng(idx(j)), "escope")
                If Len(aux) > 0 Then aux = aux + ","
                Caminhos(j) = "," + tabdtd2bd.Elem(CLng(idx(j)), "dtdtag") + "," + aux
            Next
        Else
            MsgBox "problema em ObtElemcomum"
        End If
        
        p = 1
        P1 = InStr(Caminhos(1), ",")
        P2 = 0
        k = 1
        achou = False
        While (P1 > 0) And (Not achou)
            ElemComum = Mid(Caminhos(1), p, P1 - p)
            k = 1
            P2 = 1
            While (k < QtdIdx) And (P2 > 0)
                k = k + 1
                P2 = InStr(Caminhos(k), "," + ElemComum + ",")
            Wend
            If (P2 > 0) And (k = QtdIdx) Then
                achou = True
                For j = 1 To QtdIdx
                    tabdtd2bd.Elem(CLng(idx(j)), TabGrupos.Elem(i, "elemcomum")) = ElemComum
                Next
            Else
                p = P1 + 1
                P1 = InStr(p, Caminhos(1), ",", vbBinaryCompare)
            End If
        Wend
    Next
    Set TabGrupos = Nothing
End Sub

'-----------------------------------------------------------------------
'IsFieldTag - verifica se a tag é uma tag de campo (tabela dtd2bd)
'Tag    - tag a verificar
'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Function IsFieldTag(tag As String) As Boolean
    Dim ret As Boolean
    
    If tag Like String(Len(tag), "#") Then
        ret = (tabdtd2bd.RowCounter >= CLng(tag)) And (CLng(tag) > 0)
    End If
    
    IsFieldTag = ret
End Function

