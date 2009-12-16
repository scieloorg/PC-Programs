VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClIsisDll"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Const MaxSizeArea = 60000
Const Delim = "{"
Const SEM_ERR = 0

Const MAXMFRL_COUNT = 2

Private InitializationError As Integer
Private privateContent As ClContent

Private H As Long
'Private msg      As ClMsg
Public BDPath As String
Public BDNome As String
Public IfName As String

Property Get FullPathBD() As String
    FullPathBD = BDPath + PathSep + BDNome
End Property

Property Get FullPathInv() As String
    FullPathInv = BDPath + PathSep + IfName
End Property


'-----------------------------------------------------------------------
'MfnQuantity  - retorna o total de Records na base
'Retorno    - total de Records na base
'-----------------------------------------------------------------------
Property Get MfnQuantity() As Long
    Dim ctrl As IsisRecControl
    
    If IsisRecControlMap(H, ctrl) > ZERO Then MfnQuantity = ctrl.nxtmfn - 1
End Property

'-----------------------------------------------------------------------
'Initiate - Initiate a base de dados isis
'pPath  - caminho da base
'pMst   - nome do arquivo da base
'Restart    - reinicia a base de dados
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function Initiate(pPath As String, pMst As String, Label As String, Optional Restart As Boolean) As Boolean
    Dim ret As Boolean
Dim retIsisSpaMf As Long
        
    If DirExist(pPath, Label) Then
        If Len(pMst) > 0 Then
            BDPath = pPath
            BDNome = pMst
            
            retIsisSpaMf = IsisSpaMf(H, FullPathBD)
            If retIsisSpaMf = ZERO Then
                InitializationError = SEM_ERR
                If Restart Then
                    InitializationError = IsisSpaMfCreate(H)
                End If
            ElseIf IsisSpaMf(H, FullPathBD) = ERR_FILEMASTER Then
                InitializationError = IsisSpaMfCreate(H)
            ElseIf retIsisSpaMf = ERR_PARFILNINV Then
                InitializationError = retIsisSpaMf
                MsgBox "Invalid file name size: " + FullPathBD
                
                
            End If
        End If
    End If
    If InitializationError = SEM_ERR Then
        'Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
        ret = True
    End If
    Initiate = ret
End Function

'-----------------------------------------------------------------------
'IfCreate    - Criar o arquivo invertido
'FileName   - Nome do arquivo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function IfCreate(ByVal filename As String, Optional Label As String, Optional Restart As Boolean) As Boolean
    Dim ret As Boolean
    Dim r As Long
    
    IfName = filename
    r = IsisSpaFst(H, FullPathInv)
    If r = ERR_FILEFST Then
        ret = FileExist(BDPath, IfName + ".fst", Label)
    ElseIf r = ZERO Then
        r = IsisSpaIf(H, FullPathInv)
        If r = ERR_FILEINVERT Then
            ret = (IsisSpaIfCreate(H) = ZERO)
        ElseIf r = ZERO Then
            If Restart Then
                ret = (IsisSpaIfCreate(H) = ZERO)
            Else
                ret = True
            End If
        End If
    End If
    
    If (Not ret) And (Len(Label) > 0) Then MsgBox InterfaceLabels("MsgCreationInvFileFailure").elem2 + FullPathInv
    IfCreate = ret
End Function

'-----------------------------------------------------------------------
'RecordSave - Grava em registro
'Value  - conteúdo a ser gravado
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function RecordSave(ByVal Value As String) As Long
    'Cria e grava um  registro, cujo conteúdo <Value> esteja no formato:
    '   <tag1>campo1</tag1>
    '   <tag2>campo2</tag2>
    '   <tag3>campo3</tag3>
    '   ...
    '   <tagn>campon</tagn>
    'Retorna o Mfn do registro
    Dim ret As Long
    Dim Mfn As Long
    Dim r As Long
    If InitializationError = SEM_ERR Then
        r = IsisRecShelfSize(H, 0, 3 * MAXMFRL)
        If r = ZERO Then
            Mfn = IsisRecNew(H, 0)
            If Mfn > 0 Then
                r = IsisRecRead(H, 0, Mfn)
                If r = ZERO Then
                    r = IsisRecUpdate(H, 0, Value)
                    If r = ZERO Then
                        r = IsisRecWrite(H, 0)
                        If r = ZERO Then
                            ret = Mfn
                        Else
                            msg.GiveRunInformation ("IsisRecWrite:" + CStr(r))
                        End If
                    Else
                        msg.GiveRunInformation ("IsisRecUpdate:" + CStr(r))
                        msg.GiveRunInformation (Value)
                    End If
                Else
                msg.GiveRunInformation ("IsisRecRead:" + CStr(r))
                End If
            Else
            msg.GiveRunInformation ("IsisRecNew:" + CStr(r))
            End If
        Else
        msg.GiveRunInformation ("IsisRecShelfSize:" + CStr(r))
        End If
    End If
    
    If ret = 0 Then
    msg.GiveRunInformation (InterfaceLabels("MsgFailureWriting").elem2 + CStr(Mfn) + "[" + CStr(r) + "] " & Value)
    End If

    RecordSave = ret
End Function

'-----------------------------------------------------------------------
'FieldContentUpdate - atualizar conteúdo do campo
'Mfn    - registro
'Campo  - campo
'Value  - conteúdo a ser atualizado
'Occ    - ocorrência do campo (opcional, default=1)
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function FieldContentUpdate(Mfn As Long, Campo As Long, Value As String, Optional occ) As Boolean
    Dim ocorrencia As String
    Dim ret As Boolean
    
    If IsMissing(occ) Then
        ocorrencia = "1"
    Else
        ocorrencia = CStr(occ)
    End If
        
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecFieldUpdate(H, 0, "d" + CStr(Campo) + "/" + ocorrencia) = ZERO Then
            If IsisRecFieldUpdate(H, 0, "a" + CStr(Campo) + Delim + Value + Delim) = ZERO Then
            
                If IsisRecWrite(H, 0) = ZERO Then ret = True
            End If
        End If
    
    End If
    If Not ret Then msg.GiveRunInformation (InterfaceLabels("MsgUpdateFailure").elem2 + CStr(Mfn))
    FieldContentUpdate = ret
End Function

'-----------------------------------------------------------------------
'FieldContentDel - apaga conteúdo do campo
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo (opcional, default=1)
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function FieldContentDel(Mfn As Long, Campo As Long, Optional occ) As Boolean
    Dim ocorrencia As String
    Dim ret As Boolean
    
    If IsMissing(occ) Then
        ocorrencia = "1"
    Else
        ocorrencia = CStr(occ)
    End If
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecFieldUpdate(H, 0, "d" + CStr(Campo) + "/" + ocorrencia) = ZERO Then
            
            If IsisRecWrite(H, 0) = ZERO Then ret = True
        End If
    End If
    If Not ret Then msg.GiveRunInformation (InterfaceLabels("msgDeletingFailure_Field").elem2 + CStr(Campo) + ". Mfn=" + CStr(Mfn))
    FieldContentDel = ret
End Function

'-----------------------------------------------------------------------
'IfUpdate - atualizar o arquivo invertido
'Inicio - registro inicial
'Fim    - registro final
'FlagMantido    -
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function IfUpdate(inicio As Long, fim As Long, Optional FlagMantido As Boolean) As Boolean
    Dim op As Long
    Dim r As Long
        
    
    If FlagMantido Then op = 1
        
    r = IsisRecIfUpdateEx(H, inicio, fim, op)
    
    If r = ZERO Then
        'Call IsisSpaIf(H, FullPathInv)
    Else
        msg.GiveRunInformation (InterfaceLabels("MsgInversionUpdateFailure").elem2 + IfName)
    End If
    
    IfUpdate = (r = ZERO)
End Function

'-----------------------------------------------------------------------
'RecordUpdate - atualiza o conteúdo do registro
'Mfn    - registro
'Value  - conteúdo
'Retorno    - sucesso ou fracasso
    'Escreve em um registro cujo Mfn= <mfn>, o Value <Value>
    '   <tag1>campo1</tag1>
    '   <tag2>campo2</tag2>
    '   <tag3>campo3</tag3>
    '   ...
    '   <tagn>campon</tagn>
    'Retorna sucesso ou fracasso
'-----------------------------------------------------------------------
Function RecordUpdate(Mfn As Long, Value As String) As Boolean
    Dim ret As Boolean
    Dim Mfn2 As Long
    
    If (Mfn > MfnQuantity) Then
        While Mfn2 <> Mfn
            Mfn2 = IsisRecNew(H, 0)
        Wend
    End If
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecUpdate(H, 0, Value) = ZERO Then
            ret = (IsisRecWrite(H, 0) = ZERO)
        End If
    End If
    
    If Not ret Then
        msg.GiveRunInformation (InterfaceLabels("MsgUpdateFailure").elem2 + CStr(Mfn) + " " + Value)
    End If
    RecordUpdate = ret
End Function

'-----------------------------------------------------------------------
'FieldContentAdd   - adiciona um novo campo a um registro
'Mfn    - registro
'Campo  - campo
'Value  - conteúdo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function FieldContentAdd(Mfn As Long, Campo As Long, Value As String) As Boolean
    Dim ret As Boolean
    Dim tam As Long
    Dim area As String * MaxSizeArea
    Dim v As String
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        v = "a" + CStr(Campo) + Delim + Value + Delim
        If IsisRecFieldUpdate(H, 0, v) = ZERO Then
        
            ret = (IsisRecWrite(H, 0) = ZERO)
        End If
    Else
        Debug.Print
    End If
    If Not ret Then msg.GiveRunInformation (InterfaceLabels("MsgFieldAddFailure").elem2 + CStr(Campo) + ". Mfn=" + CStr(Mfn))
    FieldContentAdd = ret
End Function

Function GetFreeRange(Begin() As Long, finish() As Long) As Long
    Dim Mfn As Long
    Dim RangeCount As Long
    
    Mfn = 0
    Erase Begin
    Erase finish
    While Mfn < MfnQuantity
        Mfn = Mfn + 1
        If FieldCount(Mfn) = 0 Then
            RangeCount = RangeCount + 1
            ReDim Preserve Begin(RangeCount)
            ReDim Preserve finish(RangeCount)
            Begin(RangeCount) = Mfn
            
            While (Mfn < MfnQuantity) And (finish(RangeCount) = 0)
                Mfn = Mfn + 1
                If FieldCount(Mfn) > 0 Then
                    finish(RangeCount) = Mfn - 1
                End If
            Wend
            
        End If
    Wend
    If RangeCount > 0 Then
        If (finish(RangeCount) = 0) And (MfnQuantity = Mfn) Then finish(RangeCount) = Mfn
    End If
    GetFreeRange = RangeCount
End Function


'-----------------------------------------------------------------------
'Recorddel    - apaga o conteúdo de um registro
'Mfn    - registro
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function RecordDel(Mfn As Long) As Boolean
    Dim ret As Boolean
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecFieldUpdate(H, 0, "d*") = ZERO Then
            If IsisRecWrite(H, 0) = ZERO Then
                ret = True
            End If
        End If
    End If
    If Not ret Then msg.GiveRunInformation (InterfaceLabels("msgRecordDeleteFailure").elem2 + CStr(Mfn))

    RecordDel = ret
End Function

'-----------------------------------------------------------------------
'RecordGet  - retorna o conteúdo do registro
'Mfn    - registro
'-----------------------------------------------------------------------
Function RecordGet(Mfn As Long) As String
    Dim area As String * MaxSizeArea
    Dim tam As Long
    Dim ret As String
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        tam = IsisRecDump(H, 0, area, MaxSizeArea)
        If tam > ZERO Then ret = Left(area, tam)
    End If
    RecordGet = ret
End Function

'-----------------------------------------------------------------------
'FieldContentOccGet - retorna o conteúdo do campo
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo no registro
'Retorno    - o conteúdo do campo
'-----------------------------------------------------------------------
Public Function FieldContentOccGet(Mfn As Long, Campo As Long, occ As Long) As String
    Dim area As String * MaxSizeArea
    Dim retorno As String
    Dim r As Long
    Dim QtdOcc As Long
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    r = IsisRecRead(H, 0, Mfn)
    If r = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
        If (QtdOcc > 0) And (occ <= QtdOcc) Then
            r = IsisRecField(H, 0, Campo, occ, area, MaxSizeArea)
            If r > ZERO Then
                retorno = Left(area, r)
                r = InStr(retorno, CONST_SUBFIELDINDICATOR)
                If r > 0 Then retorno = Mid(retorno, 1, r - 1)
            End If
        End If
    End If
    FieldContentOccGet = retorno
End Function


'-----------------------------------------------------------------------
'FieldContentGet - retorna o conteúdo do Field
'Mfn    - registro
'Field  - Field
'Occ    - ocorrência do Field no registro
'Return - o conteúdo do Field
'-----------------------------------------------------------------------
Public Function FieldContentGet(Mfn As Long, Field As Long, Contents() As String) As Long
    Dim area As String * MaxSizeArea
    Dim aux As String
    Dim r As Long
    Dim QtdOcc As Long
    Dim occ As Long
        
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    r = IsisRecRead(H, 0, Mfn)
    If r = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Field)
        ReDim Contents(QtdOcc)
        For occ = 1 To QtdOcc
            r = IsisRecField(H, 0, Field, occ, area, MaxSizeArea)
            If r > ZERO Then
                aux = Left(area, r)
                r = InStr(aux, CONST_SUBFIELDINDICATOR)
                If r > 0 Then aux = Mid(aux, 1, r - 1)
                Contents(occ) = aux
            End If
        Next
    End If
    FieldContentGet = QtdOcc
End Function
'-----------------------------------------------------------------------
'SubfieldContentGet - retorna o conteúdo do Subfield
'Mfn    - registro
'Field  - Field
'Subfield   - Subfield (uma letra)
'Contents   - conteúdo
'Retorno    - a quantidade de conteúdo
'-----------------------------------------------------------------------
Public Function SubfieldContentGet(Mfn As Long, Field As Long, SubField As String, Contents() As String) As Long
    Dim area As String * MaxSizeArea
    Dim retorno As String
    Dim r As Long
    Dim QtdOcc As Long
    Dim occ As Long
        
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    r = IsisRecRead(H, 0, Mfn)
    If r = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Field)
        ReDim Contents(QtdOcc)
        For occ = 1 To QtdOcc
            r = IsisRecSubField(H, 0, Field, occ, SubField, area, MaxSizeArea)
            If r > ZERO Then retorno = Left(area, r)
            Contents(occ) = retorno
        Next
    End If
            
    SubfieldContentGet = QtdOcc
End Function

'-----------------------------------------------------------------------
'antesFieldContentOccWithSubfieldGet
'FieldContentAllOccGet - retorna o conteúdo do campo com os subcampos
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo no registro
'Retorno    - o conteúdo do campo
'-----------------------------------------------------------------------
Public Function FieldContentAllOccGet(Mfn As Long, Campo As Long, occ As Long) As String
    Dim area As String * MaxSizeArea
    Dim retorno As String
    Dim r As Long
    Dim QtdOcc As Long
    
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    r = IsisRecRead(H, 0, Mfn)
    If r = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
        If (QtdOcc > 0) And (occ <= QtdOcc) Then
            r = IsisRecField(H, 0, Campo, occ, area, MaxSizeArea)
            If r > ZERO Then retorno = Left(area, r)
        End If
    Else
        Debug.Print

    End If
    FieldContentAllOccGet = retorno
End Function

'-----------------------------------------------------------------------
'SubFieldContentOccGet - retorna o conteúdo do subcampo
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo no registro
'Subcampo   - subcampo (uma letra)
'Retorno    - o conteúdo do subcampo
'-----------------------------------------------------------------------
Public Function SubFieldContentOccGet(Mfn As Long, Campo As Long, occ As Long, Subcampo As String) As String
    Dim area As String * MaxSizeArea
    Dim retorno As String
    Dim r As Long
    Dim QtdOcc As Long
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    r = IsisRecRead(H, 0, Mfn)
    If r = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
        If (QtdOcc > 0) And (occ <= QtdOcc) Then
            r = IsisRecSubField(H, 0, Campo, occ, Subcampo, area, MaxSizeArea)
            If r > ZERO Then retorno = Left(area, r)
        End If
    End If
            
    SubFieldContentOccGet = retorno
End Function

'-----------------------------------------------------------------------
'FieldCount   - Retorna a quantidade de campos de um registro
'Mfn    - registro
'Retorno    - a quantidade de campos
'-----------------------------------------------------------------------
Public Function FieldCount(Mfn As Long) As Long
    Dim Qtd As Long
                
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then Qtd = IsisRecNvf(H, 0)
    
    FieldCount = Qtd
End Function

'-----------------------------------------------------------------------
'TagContents - tag the content to become in format to save in records
'content    - content to tag
'Return the tagged content
'-----------------------------------------------------------------------
Function TagContents(ByVal content As String, ByVal Tag As Long) As String
    TagContents = privateContent.TagContent(content, Tag)
End Function


'-----------------------------------------------------------------------
'TagOccContentGet - obtém os Tags existentes em um registro
'Mfn    - registro
'Tags   - retorno
'Retorno    - a quantidade de Tags
'-----------------------------------------------------------------------
Public Function TagOccContentGet(Mfn As Long, Tags() As Long, Occs() As Long, Contents() As String) As Long
    Dim Qtd As Long
    Dim i As Long
    Dim j As Long
    Dim pIsisRecDir() As IsisRecDir
    Dim done() As Boolean
    Dim QtdOcc As Long
    Dim occ As Long
    Dim Campo As Long
    Dim Max As Long
    Dim tam As Long
    Dim area As String * MaxSizeArea
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        Qtd = IsisRecNvf(H, 0)
        If Qtd > 0 Then
            ReDim pIsisRecDir(Qtd)
            ReDim Tags(Qtd)
            ReDim Occs(Qtd)
            ReDim Contents(Qtd)
            If IsisRecDirMap(H, 0, 1, Qtd, pIsisRecDir(0)) > ZERO Then
                For i = 1 To Qtd
                    Campo = pIsisRecDir(i - 1).Tag
                    If Max < Campo Then
                        Max = Campo
                        ReDim Preserve done(Max)
                    End If
                    If Not done(Campo) Then
                        done(Campo) = True
                        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
                        For occ = 1 To QtdOcc
                            j = j + 1
                            tam = IsisRecField(H, 0, Campo, occ, area, MaxSizeArea)
                            Contents(j) = Left(area, tam)
                            Tags(j) = Campo
                            Occs(j) = occ
                        Next
                    End If
                Next
            End If
        End If
    Else
        Debug.Print
        
    End If
    TagOccContentGet = Qtd
End Function

'-----------------------------------------------------------------------
'FieldCount   - Retorna a quantidade (ocorrência) de um determinado campo de um registro
'Mfn    - registro
'Campo  - campo
'Retorno    - ocorrência
'-----------------------------------------------------------------------
Public Function FieldOccCount(Mfn As Long, Campo As Long) As Long
    Dim QtdOcc As Long
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
    Else
        Debug.Print
    End If
    FieldOccCount = QtdOcc
End Function

'-----------------------------------------------------------------------
'MfnFind   - retorna os Mfns dos Records correspondentes às chaves
'Termo  - chave
'Mfns   - os Mfns encontrados
'Retorno    - a quantidade de Mfns
'-----------------------------------------------------------------------
Public Function MfnFind(ByVal Termo As String, Mfns() As Long) As Long
    Dim i As Long
    Dim QtdTrm As Long
    Dim pIsisTrmMfn() As IsisTrmMfn
    Dim pIsisTrmRead As IsisTrmRead
    Dim exist As Boolean
    Dim j As Long
    Dim MfnsCount As Long
    
    
    
    
    'Call IsisSpaIf(H, FullPathInv)
    Erase Mfns
    pIsisTrmRead.key = Termo
    QtdTrm = IsisTrmReadMap(H, 0, pIsisTrmRead)
    If QtdTrm > ZERO Then
                ReDim pIsisTrmMfn(QtdTrm)
                QtdTrm = IsisTrmMfnMap(H, 0, 1, QtdTrm, pIsisTrmMfn(0))
        
                For i = 1 To QtdTrm
                    j = 0
                    exist = False
                    While (j < MfnsCount) And (Not exist)
                        j = j + 1
                        exist = (pIsisTrmMfn(i - 1).Mfn = Mfns(j))
                    Wend
                    If Not exist Then
                        MfnsCount = MfnsCount + 1
                        ReDim Preserve Mfns(MfnsCount)
                        Mfns(i) = pIsisTrmMfn(i - 1).Mfn
                    End If
                Next
    End If
    
    MfnFind = MfnsCount
End Function

Public Function GetTerms(Terms() As String, format As String) As Long
    Dim area As String
    Dim QtdTrm As Long
    Dim i As Long
    
    QtdTrm = 0
    Erase Terms
    
    For i = 1 To MfnQuantity
        area = UsePft(i, format)
        If Len(area) > 0 Then
            QtdTrm = QtdTrm + 1
            ReDim Preserve Terms(QtdTrm)
            Terms(QtdTrm) = area
        End If
    Next
    GetTerms = QtdTrm
End Function

'-----------------------------------------------------------------------
'AmpliarIntervaloLivre  - dado um intervalo, amplia este se houver Records vazios nas proximidades
'ini    - limite inferior
'fim    - limite superior
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function AmpliarIntervaloLivre(ini As Long, fim As Long) As Boolean
    Dim Preenchido As Long
    Dim InicioInterv As Long
    Dim FimInterv As Long
    Dim ret As Boolean
    
    InicioInterv = ini
    Preenchido = 0
    While (Preenchido = 0) And (InicioInterv - 1 > 1)
        Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
        If IsisRecRead(H, 0, InicioInterv - 1) = ZERO Then
            Preenchido = IsisRecNvf(H, 0)
            If Preenchido = 0 Then InicioInterv = InicioInterv - 1
        End If
    Wend
    If ini > InicioInterv Then
        ini = InicioInterv
        ret = True
    End If
        
    FimInterv = fim
    Preenchido = 0
    While (Preenchido = 0) And (FimInterv + 1 <= MfnQuantity)
        Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
        If IsisRecRead(H, 0, FimInterv + 1) = ZERO Then
            Preenchido = IsisRecNvf(H, 0)
            If Preenchido = 0 Then FimInterv = FimInterv + 1
        End If
    Wend
    If fim < FimInterv Then
        fim = FimInterv
        ret = ret Or True
    End If
        
    AmpliarIntervaloLivre = ret
End Function

Private Sub Class_Initialize()
    H = IsisSpaNew(AppHandle)
    InitializationError = -1
    Set privateContent = New ClContent
End Sub

Private Sub Class_Terminate()
    IsisSpaDelete (H)
End Sub


Public Function BDClean() As Boolean
    Dim deleted As Long
    Dim TmpFile As String
    Dim tmp As ClIsisDll
    Dim Mfn As Long
    Dim q As Long
    Dim content As String
    
    TmpFile = BDNome + "TMP"
        
    Call msg.GiveRunInformation(InterfaceLabels("MsgRemoveEmptyRecords").elem2, , True)
    FormMarkup.ProgressBar1.Visible = True
    

    Call FileCopy(BDPath + PathSep + BDNome + ".mst", BDPath + PathSep + TmpFile + ".mst")
    Call FileCopy(BDPath + PathSep + BDNome + ".xrf", BDPath + PathSep + TmpFile + ".xrf")
    
    If Initiate(BDPath, BDNome, "", True) Then
        If IfCreate(IfName, , True) Then
            Set tmp = New ClIsisDll
            If tmp.Initiate(BDPath, TmpFile, "") Then
                q = tmp.MfnQuantity
                For Mfn = 1 To q
                    FormMarkup.ProgressBar1.Value = (Mfn / q) * FormMarkup.ProgressBar1.Max
                    content = tmp.RecordGet(Mfn)
                    If Len(content) > 0 Then
                        RecordSave (content)
                    Else
                        deleted = deleted + 1
                    End If
                Next
                Call IfUpdate(1, MfnQuantity)
            End If
            Set tmp = Nothing
        End If
    End If
    Kill BDPath + "\" + TmpFile + ".*"
    FormMarkup.ProgressBar1.Visible = False
    
    BDClean = (q = deleted + MfnQuantity)
End Function
Public Function Old_BDClean() As Boolean
    Dim deleted As Long
    Dim TmpFile As String
    Dim tmp As ClIsisDll
    Dim Mfn As Long
    Dim q As Long
    
    TmpFile = BDNome + "TMP"
        
    Call msg.GiveRunInformation(InterfaceLabels("MsgRemoveEmptyRecords").elem2, , True)
    FormMarkup.ProgressBar1.Visible = True
    
    Call FileCopy(BDPath + PathSep + BDNome + ".mst", BDPath + PathSep + TmpFile + ".mst")
    Call FileCopy(BDPath + PathSep + BDNome + ".xrf", BDPath + PathSep + TmpFile + ".xrf")
    
    If Initiate(BDPath, BDNome, "", True) Then
        If IfCreate(BDNome, , True) Then
            Set tmp = New ClIsisDll
            If tmp.Initiate(BDPath, TmpFile, "") Then
                q = tmp.MfnQuantity
                For Mfn = 1 To q
                    FormMarkup.ProgressBar1.Value = (Mfn / q) * FormMarkup.ProgressBar1.Max
                    If tmp.FieldCount(Mfn) > 0 Then
                        RecordSave (tmp.RecordGet(Mfn))
                    Else
                        deleted = deleted + 1
                    End If
                Next
                Call IfUpdate(1, MfnQuantity)
            End If
            Set tmp = Nothing
        End If
    End If
    Kill BDPath + "\" + TmpFile + ".*"
    FormMarkup.ProgressBar1.Visible = False
    
    Old_BDClean = (q = deleted + MfnQuantity)
End Function

'-----------------------------------------------------------------------
'BDDel  - apaga a base de dados
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function BDDel() As Boolean
    Dim ret As Boolean
    Dim i As Long
    
    For i = 1 To MfnQuantity
        RecordDel (i)
    Next
    If IfUpdate(1, MfnQuantity) Then
        ret = Initiate(BDPath, BDNome, "", True)
    End If
        
    BDDel = ret
End Function

'-----------------------------------------------------------------------
'BDConvert2ISO  -
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function BDConvert2ISO() As Boolean
    Dim Mfn As Long
    Dim isocount As Long
    
    If IsisSpaIsoOut(H, BDPath + PathSep + BDNome) = ZERO Then
        If IsisSpaIsoOutCreate(H) = ZERO Then
            
            While (Mfn < MfnQuantity)
                Mfn = Mfn + 1
                Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
                If IsisRecRead(H, 0, Mfn) = ZERO Then
                    If IsisRecNvf(H, 0) > ZERO Then
                        If IsisRecIsoWrite(H, 0) > ZERO Then
                            isocount = isocount + 1
                        End If
                    End If
                End If
            Wend
        End If
    End If
    BDConvert2ISO = (isocount > 0)
End Function

Function RecordCopy(SourceMfn As Long, DestinyBD As ClIsisDll, DestinyMfn As Long) As Boolean
    Dim ret As Boolean
    Dim Registro As String
    
    'Obtenção do registro
    If (SourceMfn > 0) And (SourceMfn <= MfnQuantity) Then
        Registro = RecordGet(SourceMfn)
    
        If (DestinyMfn = 0) Then
            DestinyMfn = DestinyBD.RecordSave(Registro)
            ret = (DestinyMfn > 0)
        Else
            ret = DestinyBD.RecordUpdate(DestinyMfn, Registro)
        End If
    
        If ret Then
            If Not DestinyBD.IfUpdate(DestinyMfn, DestinyMfn) Then
                Call msg.GiveRunInformation(InterfaceLabels("MsgDatabaseUpdateFailure").elem2 + DestinyBD.BDNome)
                ret = False
            End If
        Else
            Call msg.GiveRunInformation(InterfaceLabels("MsgRecordCopyFailure").elem2)
        End If
    End If
    RecordCopy = ret
End Function

Function MfnFindOne(Chave As String) As Long
    Dim xMfn() As Long
    Dim Mfn As Long
    Dim i As Long
    
    i = MfnFind(Chave, xMfn)
    If i > 0 Then Mfn = xMfn(i)
        
    MfnFindOne = Mfn
End Function

Function Save(Contents As String, Mfn As Long) As Boolean
    Dim ret As Boolean
    
    If Mfn = 0 Then
        Mfn = RecordSave(Contents)
        If Mfn > 0 Then ret = IfUpdate(Mfn, Mfn)
    Else
        If RecordUpdate(Mfn, Contents) Then ret = IfUpdate(Mfn, Mfn)
    End If
    Save = ret
End Function


'-----------------------------------------------------------------------
'nao existe no conversor
'FieldTagGet - obtém os campos existentes em um registro
'Mfn    - registro
'Campos - retorno
'Retorno    - a quantidade de campos
'-----------------------------------------------------------------------
Public Function FieldTagGet(Mfn As Long, Campos() As Long) As Long
    Dim Qtd As Long
    Dim i As Long
    Dim pIsisRecDir() As IsisRecDir
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        Qtd = IsisRecNvf(H, 0)
        ReDim pIsisRecDir(Qtd)
        ReDim Campos(Qtd)
        Call IsisRecDirMap(H, 0, 1, Qtd, pIsisRecDir(0))
        For i = 1 To Qtd
            Campos(i) = pIsisRecDir(i - 1).Tag
        Next
        Else
            Debug.Print
    End If
    FieldTagGet = Qtd
End Function


'-----------------------------------------------------------------------
'nao existe no conversor
'antesFieldContentGetAll
'FieldContentAllGet - retorna o conteúdo do Field
'Mfn    - registro
'Field  - Field
'Occ    - ocorrência do Field no registro
'Return - o conteúdo do Field
'-----------------------------------------------------------------------
Public Function FieldContentAllGet(Mfn As Long, Field As Long, Contents() As String) As Long
    Dim area As String * MaxSizeArea
    Dim r As Long
    Dim QtdOcc As Long
    Dim occ As Long
    
    Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
    r = IsisRecRead(H, 0, Mfn)
    If r = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Field)
        ReDim Contents(QtdOcc)
        For occ = 1 To QtdOcc
            r = IsisRecField(H, 0, Field, occ, area, MaxSizeArea)
            If r > ZERO Then Contents(occ) = Left(area, r)
        Next
        Else
            Debug.Print
    
    End If
    FieldContentAllGet = QtdOcc
End Function

Sub Gizmo(File As String)
    Dim Mfn As Long
'    Dim fn As Long
'    Dim FileName As String
    Dim P As Long
    Dim NewValue As String
    Dim area As String * MaxSizeArea
    Dim tam As Long
              
    If IsisSpaGf(H, File) = ZERO Then
        Call IsisSpaGf(H, File)
        For Mfn = 1 To MfnQuantity
            Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
            If IsisRecRead(H, 0, Mfn) = ZERO Then
                tam = IsisRecDump(H, 0, area, MaxSizeArea)
                If tam > ZERO Then
                    NewValue = Left(area, tam)
                    'Print #fn, NewValue
                    If IsisRecUpdate(H, 0, NewValue) = ZERO Then
                        If IsisRecWrite(H, 0) <> ZERO Then
                        End If
                    End If
                End If
            Else
                Debug.Print
            End If
        Next
    End If
    'Close fn
End Sub

Public Function UsePft(Mfn As Long, format As String) As String
    Dim area As String * MaxSizeArea
    Dim ResultLen As Long
    Dim result As String
    Dim fn As Long
                
        If IsisSpaPftCisis(H, format) = ZERO Then
            Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
            If IsisRecRead(H, 0, Mfn) = ZERO Then
                ResultLen = IsisRecFormatCisis(H, 0, area, MaxSizeArea)
                If ResultLen > 0 Then result = Left(area, ResultLen)
            End If
        End If
    UsePft = result
End Function

Public Function UseProc(Mfn As Long, format As String) As Boolean
    Dim ret As Boolean
    
        Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
        If IsisRecRead(H, 0, Mfn) = ZERO Then
            If IsisRecFieldUpdate(H, 0, format) = ZERO Then
                If IsisRecWrite(H, 0) = ZERO Then ret = True
            End If
        End If
    
    UseProc = ret
End Function

Private Function ListKeys() As String
    Dim i As Long
    Dim List As String
    Dim QtdTrm As Long
    Dim pIsisTrmMfn() As IsisTrmMfn
    Dim pIsisTrmRead As IsisTrmRead
    Dim exist As Boolean
    Dim j As Long
    Dim MfnsCount As Long
    

    pIsisTrmRead.key = ""
    
    QtdTrm = IsisTrmReadMap(H, 0, pIsisTrmRead)
    List = "List Keys of " + FullPathInv + vbCrLf
    While QtdTrm <> ERR_TRMEOF
        MfnsCount = MfnsCount + 1
        List = List + "Key[" + CStr(MfnsCount) + "]=" + pIsisTrmRead.key + vbCrLf
        QtdTrm = IsisTrmReadNext(H, 0, pIsisTrmRead)
    Wend
    
    ListKeys = List
End Function

Function DoSearch(query As String, Mfns() As Long) As Long
    Dim i As Long
    Dim pIsisSrcHeader As IsisSrcHeader
    Dim pIsisSrcMfn() As IsisSrcMfn
    Dim r As Long
    
    r = IsisSrcSearch(H, 0, query, pIsisSrcHeader)
    If r > 0 Then
        ReDim pIsisSrcMfn(pIsisSrcHeader.recs)
        r = IsisSrcMfnMap(AppHandle, 0, 0, 1, pIsisSrcHeader.recs, pIsisSrcMfn(0))
        If r > 0 Then
            For i = 1 To pIsisSrcHeader.recs
                ReDim Preserve Mfns(i)
                Mfns(i) = pIsisSrcMfn(i - 1).Mfn
            Next
        End If
    End If
    
    DoSearch = pIsisSrcHeader.recs
End Function

Function deleteRecordRange(inicio As Long, fim As Long) As Boolean
    Dim ret As Boolean
    Dim Mfn As Long
    Dim r As Long
    
    If (inicio > 0) And (fim >= inicio) Then
    For Mfn = inicio To fim
        Call IsisRecShelfSize(H, 0, 3 * MAXMFRL)
        If IsisRecRead(H, 0, Mfn) = ZERO Then
            If IsisRecFieldUpdate(H, 0, "d.") = ZERO Then
                If IsisRecWrite(H, 0) = ZERO Then
                    If IsisRecIfUpdate(H, Mfn) = ZERO Then
                        ret = True
                    End If
                End If
            End If
        End If
    Next
    'r = IsisRecLnk(H, 1, 9999999)   ' link generation
    'r = IsisLnkSort(H) ' sort of the links
    'r = IsisLnkIfLoad(H)  ' load proces
    End If
    
    deleteRecordRange = ret
End Function

Sub buildExpression(Prefix As String, term As String, values() As String, i As Long)
    If Len(Trim(term)) > 0 Then
        
        ReDim Preserve values(i)
        values(i) = Prefix + term
        i = i + 1
    End If
End Sub
