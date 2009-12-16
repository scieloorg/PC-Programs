VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClIsisDll"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Const MaxTamArea = 30000
Const Delim = "{"
Const SEM_ERR = 0
Const PathSep = "\"
Private Msg As ClMsg
Private ErroIniciacao As Integer

Private H As Long
Private Path As String
Private Nome As String
Private ArqInv As String


Property Let BDPath(v As String)
    Path = v
End Property
Property Get BDPath() As String
    BDPath = Path
End Property
Property Get FullPathBD() As String
    FullPathBD = Path + PathSep + Nome
End Property
Property Get FullPathInv() As String
    FullPathInv = Path + PathSep + IfName
End Property
Property Let BDNome(v As String)
    Nome = v
End Property
Property Get BDNome() As String
    BDNome = Nome
End Property
Property Let IfName(v As String)
    ArqInv = v
End Property
Property Get IfName() As String
    IfName = ArqInv
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
'Inicia - Inicia a base de dados isis
'pPath  - caminho da base
'pMst   - nome do arquivo da base
'Restart    - reinicia a base de dados
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function Inicia(pPath As String, pMst As String, label As String, Optional Restart As Boolean) As Boolean
    Dim Ret As Boolean
    
    If DirExist(pPath, label) Then
        If Len(pMst) > 0 Then
            BDPath = pPath
            BDNome = pMst
            If IsisSpaMf(H, FullPathBD) = ERR_FILEMASTER Then
                ErroIniciacao = IsisSpaMfCreate(H)
            Else
                ErroIniciacao = SEM_ERR
                If Restart Then ErroIniciacao = IsisSpaMfCreate(H)
            End If
        End If
    End If
    If ErroIniciacao = SEM_ERR Then
        'Call IsisRecShelfSize(H, 0, 2 * MAXMFRL)
        Ret = True
    End If
    Inicia = Ret
End Function

'-----------------------------------------------------------------------
'IfCreate    - Criar o arquivo invertido
'FileName   - Nome do arquivo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function IfCreate(ByVal FileName As String, Optional Clear As Boolean) As Boolean
    Dim Ret As Boolean
    Dim R As Long
    
    IfName = FileName
    R = IsisSpaFst(H, FullPathInv)
    If R = ERR_FILEFST Then
        Ret = FileExist(BDPath, IfName + ".fst", "Inverted File")
    ElseIf R = ZERO Then
        R = IsisSpaIf(H, FullPathInv)
        If (R = ERR_FILEINVERT) Or Clear Then
            Ret = (IsisSpaIfCreate(H) = ZERO)
        ElseIf R = ZERO Then
            Ret = True
        End If
    End If
    If Not Ret Then MsgBox "Failure creating inverted file " + FullPathInv
    IfCreate = Ret
End Function

'-----------------------------------------------------------------------
'RecordSave - Grava em registro
'Value  - conteúdo a ser gravado
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function RecordSave(ByVal value As String) As Long
    'Cria e grava um  registro, cujo conteúdo <Value> esteja no formato:
    '   <tag1>campo1</tag1>
    '   <tag2>campo2</tag2>
    '   <tag3>campo3</tag3>
    '   ...
    '   <tagn>campon</tagn>
    'Retorna o Mfn do registro
    Dim ctrl As IsisRecControl
    Dim Ret As Long
    Dim Mfn As Long
    
    If ErroIniciacao = SEM_ERR Then
        Mfn = IsisRecNew(H, 0)
        If Mfn > ZERO Then
            If RecordUpdate(Mfn, value) Then
                Ret = Mfn
            Else
                Msg.GiveRunInformation ("Failure writing Mfn=" + CStr(Mfn))
            End If
        End If
    End If
    RecordSave = Ret
End Function

'-----------------------------------------------------------------------
'FieldContentUpdate - atualizar conteúdo do campo
'Mfn    - registro
'Campo  - campo
'Value  - conteúdo a ser atualizado
'Occ    - ocorrência do campo (opcional, default=1)
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function FieldContentUpdate(Mfn As Long, Campo As Long, value As String, Optional Occ) As Boolean
    Dim ocorrencia As String
    Dim Ret As Boolean
    
    If IsMissing(Occ) Then
        ocorrencia = "1"
    Else
        ocorrencia = CStr(Occ)
    End If
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecFieldUpdate(H, 0, "d" + CStr(Campo) + "/" + ocorrencia) = ZERO Then
            If IsisRecFieldUpdate(H, 0, "a" + CStr(Campo) + Delim + value + Delim) = ZERO Then
            'Msg.GiveRunInformation ("Mfn=" + CStr(Mfn))
                If IsisRecWrite(H, 0) = ZERO Then Ret = True
            End If
        End If
    End If
    If Not Ret Then Msg.GiveRunInformation ("Failure updating Mfn=" + CStr(Mfn))
    FieldContentUpdate = Ret
End Function

'-----------------------------------------------------------------------
'FieldContentDel - apaga conteúdo do campo
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo (opcional, default=1)
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function FieldContentDel(Mfn As Long, Campo As Long, Optional Occ) As Boolean
    Dim ocorrencia As String
    Dim Ret As Boolean
    
    If IsMissing(Occ) Then
        ocorrencia = "1"
    Else
        ocorrencia = CStr(Occ)
    End If
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecFieldUpdate(H, 0, "d" + CStr(Campo) + "/" + ocorrencia) = ZERO Then
            'Msg.GiveRunInformation ("Mfn=" + CStr(Mfn))
            If IsisRecWrite(H, 0) = ZERO Then Ret = True
        End If
    End If
    If Not Ret Then Msg.GiveRunInformation ("Failure deleting field " + CStr(Campo) + " in Mfn=" + CStr(Mfn))
    FieldContentDel = Ret
End Function

'-----------------------------------------------------------------------
'IfUpdate - atualizar o arquivo invertido
'Inicio - registro inicial
'Fim    - registro final
'FlagMantido    -
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function IfUpdate(Inicio As Long, Fim As Long, Optional FlagMantido As Boolean) As Boolean
    Dim op As Long
    Dim R As Long
    
    If FlagMantido Then op = 1
    R = IsisRecIfUpdateEx(H, Inicio, Fim, op)
    Call IsisSpaIf(H, FullPathInv)
    If R <> ZERO Then Msg.GiveRunInformation ("Failure updating inverted file " + IfName)
    IfUpdate = (R = ZERO)
End Function

'-----------------------------------------------------------------------
'RecordUpdate - atualiza o conteúdo do registro
'Mfn    - registro
'Value  - conteúdo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function RecordUpdate(Mfn As Long, value As String) As Boolean
    'Escreve em um registro cujo Mfn= <mfn>, o Value <Value>
    '   <tag1>campo1</tag1>
    '   <tag2>campo2</tag2>
    '   <tag3>campo3</tag3>
    '   ...
    '   <tagn>campon</tagn>
    'Retorna sucesso ou fracasso
    Dim Ret As Boolean
    
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecUpdate(H, 0, value) = ZERO Then
        'Msg.GiveRunInformation ("Mfn=" + CStr(Mfn))
            Ret = (IsisRecWrite(H, 0) = ZERO)
        End If
    End If
    If Not Ret Then Msg.GiveRunInformation ("Failure updating Mfn=" + CStr(Mfn))
    RecordUpdate = Ret
End Function

'-----------------------------------------------------------------------
'FieldContentAdd   - adiciona um novo campo a um registro
'Mfn    - registro
'Campo  - campo
'Value  - conteúdo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function FieldContentAdd(Mfn As Long, Campo As Long, value As String) As Boolean
    'Escreve em um registro cujo Mfn= <mfn>, o Value <Value>
    Dim Ret As Boolean
    Dim tam As Long
    Dim area As String * MaxTamArea
    Dim v As String
    
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        v = "a" + CStr(Campo) + Delim + value + Delim
        If IsisRecFieldUpdate(H, 0, v) = ZERO Then
        'Msg.GiveRunInformation ("Mfn=" + CStr(Mfn))
            Ret = (IsisRecWrite(H, 0) = ZERO)
        End If
    End If
    If Not Ret Then Msg.GiveRunInformation ("Failure adding field " + CStr(Campo) + " in Mfn=" + CStr(Mfn))
    FieldContentAdd = Ret
End Function

'-----------------------------------------------------------------------
'RecordDel    - apaga o conteúdo de um registro
'Mfn    - registro
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function Recorddel(Mfn As Long) As Boolean
    Dim Ret As Boolean
       
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        If IsisRecFieldUpdate(H, 0, "d*") = ZERO Then
        'Msg.GiveRunInformation ("Mfn=" + CStr(Mfn))
            If IsisRecWrite(H, 0) = ZERO Then
                Ret = True
            End If
        End If
    End If
    If Not Ret Then Msg.GiveRunInformation ("Failure deleting record Mfn=" + CStr(Mfn))

    Recorddel = Ret
End Function

'-----------------------------------------------------------------------
'RecordGet  - retorna o conteúdo do registro
'Mfn    - registro
'-----------------------------------------------------------------------
Function RecordGet(Mfn As Long) As String
    Dim area As String * MaxTamArea
    Dim tam As Long
    Dim Ret As String
    
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        tam = IsisRecDump(H, 0, area, MaxTamArea)
        If tam > ZERO Then Ret = Left(area, tam)
    End If
    RecordGet = Ret
End Function

'-----------------------------------------------------------------------
'FieldContentOccGet - retorna o conteúdo do campo
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo no registro
'Retorno    - o conteúdo do campo
'-----------------------------------------------------------------------
Public Function FieldContentOccGet(Mfn As Long, Campo As Long, Occ As Long) As String
    Dim area As String * MaxTamArea
    Dim retorno As String
    Dim R As Long
    Dim QtdOcc As Long
    
    R = IsisRecRead(H, 0, Mfn)
    If R = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
        If (QtdOcc > 0) And (Occ <= QtdOcc) Then
            R = IsisRecField(H, 0, Campo, Occ, area, MaxTamArea)
            If R > ZERO Then
                retorno = Left(area, R)
                R = InStr(retorno, "^")
                If R > 0 Then retorno = Mid(retorno, 1, R - 1)
            End If
        End If
    End If
    FieldContentOccGet = retorno
End Function


'-----------------------------------------------------------------------
'FieldContentGetall - retorna o conteúdo do Field
'Mfn    - registro
'Field  - Field
'Occ    - ocorrência do Field no registro
'Return - o conteúdo do Field
'-----------------------------------------------------------------------
Public Function FieldContentGet(Mfn As Long, Field As Long, Contents() As String) As Long
    Dim area As String * MaxTamArea
    Dim aux As String
    Dim R As Long
    Dim QtdOcc As Long
    Dim Occ As Long
    
    R = IsisRecRead(H, 0, Mfn)
    If R = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Field)
        ReDim Contents(QtdOcc)
        For Occ = 1 To QtdOcc
            R = IsisRecField(H, 0, Field, Occ, area, MaxTamArea)
            If R > ZERO Then
                aux = Left(area, R)
                R = InStr(aux, "^")
                If R > 0 Then aux = Mid(aux, 1, R - 1)
                Contents(Occ) = aux
            End If
        Next
    End If
    FieldContentGet = QtdOcc
End Function

'-----------------------------------------------------------------------
'FieldContentGetall - retorna o conteúdo do Field
'Mfn    - registro
'Field  - Field
'Occ    - ocorrência do Field no registro
'Return - o conteúdo do Field
'-----------------------------------------------------------------------
Public Function FieldContentGetAll(Mfn As Long, Field As Long, Contents() As String) As Long
    Dim area As String * MaxTamArea
    Dim aux As String
    Dim R As Long
    Dim QtdOcc As Long
    Dim Occ As Long
    
    R = IsisRecRead(H, 0, Mfn)
    If R = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Field)
        ReDim Contents(QtdOcc)
        For Occ = 1 To QtdOcc
            R = IsisRecField(H, 0, Field, Occ, area, MaxTamArea)
            If R > ZERO Then Contents(Occ) = Left(area, R)
        Next
    End If
    FieldContentGetAll = QtdOcc
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
    Dim area As String * MaxTamArea
    Dim retorno As String
    Dim R As Long
    Dim QtdOcc As Long
    Dim Occ As Long
    
    R = IsisRecRead(H, 0, Mfn)
    If R = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Field)
        ReDim Contents(QtdOcc)
        For Occ = 1 To QtdOcc
            R = IsisRecSubField(H, 0, Field, Occ, SubField, area, MaxTamArea)
            If R > ZERO Then retorno = Left(area, R)
            Contents(Occ) = retorno
        Next
    End If
            
    SubfieldContentGet = QtdOcc
End Function

'-----------------------------------------------------------------------
'SubFieldContentOccGet - retorna o conteúdo do campo com os subcampos
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo no registro
'Retorno    - o conteúdo do campo
'-----------------------------------------------------------------------
Public Function FieldContentOccWithSubfieldGet(Mfn As Long, Campo As Long, Occ As Long) As String
    Dim area As String * MaxTamArea
    Dim retorno As String
    Dim R As Long
    Dim QtdOcc As Long
    
    R = IsisRecRead(H, 0, Mfn)
    If R = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
        If (QtdOcc > 0) And (Occ <= QtdOcc) Then
            R = IsisRecField(H, 0, Campo, Occ, area, MaxTamArea)
            If R > ZERO Then retorno = Left(area, R)
        End If
    End If
    FieldContentOccWithSubfieldGet = retorno
End Function

'-----------------------------------------------------------------------
'SubFieldContentOccGet - retorna o conteúdo do subcampo
'Mfn    - registro
'Campo  - campo
'Occ    - ocorrência do campo no registro
'Subcampo   - subcampo (uma letra)
'Retorno    - o conteúdo do subcampo
'-----------------------------------------------------------------------
Public Function SubFieldContentOccGet(Mfn As Long, Campo As Long, Occ As Long, Subcampo As String) As String
    Dim area As String * MaxTamArea
    Dim retorno As String
    Dim R As Long
    Dim QtdOcc As Long
    
    R = IsisRecRead(H, 0, Mfn)
    If R = ZERO Then
        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
        If (QtdOcc > 0) And (Occ <= QtdOcc) Then
            R = IsisRecSubField(H, 0, Campo, Occ, Subcampo, area, MaxTamArea)
            If R > ZERO Then retorno = Left(area, R)
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
                
    If IsisRecRead(H, 0, Mfn) = ZERO Then Qtd = IsisRecNvf(H, 0)

    FieldCount = Qtd
End Function

'-----------------------------------------------------------------------
'FieldTagGet - obtém os campos existentes em um registro
'Mfn    - registro
'Campos - retorno
'Retorno    - a quantidade de campos
'-----------------------------------------------------------------------
Public Function FieldTagGet(Mfn As Long, Campos() As Long) As Long
    Dim Qtd As Long
    Dim i As Long
    Dim pIsisRecDir() As IsisRecDir
    
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        Qtd = IsisRecNvf(H, 0)
        ReDim pIsisRecDir(Qtd)
        ReDim Campos(Qtd)
        Call IsisRecDirMap(H, 0, 1, Qtd, pIsisRecDir(0))
        For i = 1 To Qtd
            Campos(i) = pIsisRecDir(i - 1).tag
        Next
    End If
    FieldTagGet = Qtd
End Function

'-----------------------------------------------------------------------
'ContentAllGet - obtém os Conteudo existentes em um registro
'Mfn    - registro
'Conteudo   - retorno
'Retorno    - a quantidade de Conteudo
'-----------------------------------------------------------------------
Public Function ContentAllGet(Mfn As Long, conteudo() As String, ComSubc As Boolean) As Long
    Dim Qtd As Long
    Dim i As Long
    Dim j As Long
    Dim p As Long
    Dim aux As String
    Dim pIsisRecDir() As IsisRecDir
    Dim Occ() As Long
    Dim QtdOcc As Long
    Dim Campo As Long
    
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        Qtd = IsisRecNvf(H, 0)
        ReDim pIsisRecDir(Qtd)
        ReDim conteudo(Qtd)
        If IsisRecDirMap(H, 0, 1, Qtd, pIsisRecDir(0)) > ZERO Then
            If ComSubc Then
                For i = 1 To Qtd
                    Campo = pIsisRecDir(i - 1).tag
                    If QtdOcc < Campo Then
                        QtdOcc = Campo
                        ReDim Preserve Occ(QtdOcc)
                    End If
                    Occ(Campo) = Occ(Campo) + 1
                    aux = FieldContentOccGet(Mfn, Campo, Occ(Campo))
                    p = InStr(aux, "^")
                    While p > 0
                        j = j + 1
                        ReDim Preserve conteudo(j)
                        conteudo(j) = Mid(aux, 1, p - 1)
                        aux = Mid(aux, p + 2)
                        p = InStr(aux, "^")
                    Wend
                    j = j + 1
                    ReDim Preserve conteudo(j)
                    conteudo(j) = Mid(aux, 1)
                    Qtd = j
                Next
            Else
                For i = 1 To Qtd
                    Campo = pIsisRecDir(i - 1).tag
                    If QtdOcc < Campo Then
                        QtdOcc = Campo
                        ReDim Preserve Occ(QtdOcc)
                    End If
                    Occ(Campo) = Occ(Campo) + 1
                    conteudo(i) = FieldContentOccGet(Mfn, Campo, Occ(Campo))
                Next
            End If
        End If
    End If
    ContentAllGet = Qtd
End Function

'-----------------------------------------------------------------------
'FieldCount   - Retorna a quantidade (ocorrência) de um determinado campo de um registro
'Mfn    - registro
'Campo  - campo
'Retorno    - ocorrência
'-----------------------------------------------------------------------
Public Function FieldOccCount(Mfn As Long, Campo As Long) As Long
    Dim QtdOcc As Long
    
    If IsisRecRead(H, 0, Mfn) = ZERO Then QtdOcc = IsisRecFieldOcc(H, 0, Campo)
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

    pIsisTrmRead.Key = Termo
    
'    Call IsisSpaFst(H, FullPathInv) sem eles resolve Cisis\low level track... dbopen...
'    Call IsisSpaIf(H, FullPathInv)
    
    QtdTrm = IsisTrmReadMap(H, 0, pIsisTrmRead)
    If QtdTrm > ZERO Then
        ReDim pIsisTrmMfn(QtdTrm)
        QtdTrm = IsisTrmMfnMap(H, 0, 1, QtdTrm, pIsisTrmMfn(0))
        If QtdTrm > 0 Then ReDim Mfns(QtdTrm)
        For i = 1 To QtdTrm
            Mfns(i) = pIsisTrmMfn(i - 1).Mfn
        Next
    Else
        QtdTrm = 0
    End If
    MfnFind = QtdTrm
End Function

Public Function GetTerms(Terms() As String, format As String) As Long
    Dim pIsisTrmMfn As IsisTrmMfn
    Dim pIsisTrmRead As IsisTrmRead
    Dim area As String * 1000
    Dim R As Long
    Dim R1 As Long
    Dim QtdTrm As Long
    
    QtdTrm = 0
    Erase Terms
    
    If IsisSpaMf(H, FullPathBD) = ZERO Then
        If IsisSpaIf(H, FullPathInv) = ZERO Then
            R1 = IsisSpaPftCisis(H, format)
            pIsisTrmRead.Key = ""
            R1 = IsisTrmReadMap(H, 0, pIsisTrmRead)
            While R <> ERR_TRMEOF
                R1 = IsisTrmMfnMap(H, 0, 1, 1, pIsisTrmMfn)
                R1 = IsisRecRead(H, 0, pIsisTrmMfn.Mfn)
                R1 = IsisRecFormatCisis(H, 0, area, 900)
                QtdTrm = QtdTrm + 1
                ReDim Preserve Terms(QtdTrm)
                Terms(QtdTrm) = Left(area, R1)
                R = IsisTrmReadNext(H, 0, pIsisTrmRead)
            Wend
        End If
    End If
    GetTerms = QtdTrm
End Function

'-----------------------------------------------------------------------
'AmpliarIntervaloLivre  - dado um intervalo, amplia este se houver Records vazios nas proximidades
'ini    - limite inferior
'fim    - limite superior
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function AmpliarIntervaloLivre(ini As Long, Fim As Long) As Boolean
    Dim Preenchido As Long
    Dim InicioInterv As Long
    Dim FimInterv As Long
    Dim Ret As Boolean
    
    InicioInterv = ini
    Preenchido = 0
    While (Preenchido = 0) And (InicioInterv - 1 > 1)
        If IsisRecRead(H, 0, InicioInterv - 1) = ZERO Then
            Preenchido = IsisRecNvf(H, 0)
            If Preenchido = 0 Then InicioInterv = InicioInterv - 1
        End If
    Wend
    If ini > InicioInterv Then
        ini = InicioInterv
        Ret = True
    End If
        
    FimInterv = Fim
    Preenchido = 0
    While (Preenchido = 0) And (FimInterv + 1 <= MfnQuantity)
        If IsisRecRead(H, 0, FimInterv + 1) = ZERO Then
            Preenchido = IsisRecNvf(H, 0)
            If Preenchido = 0 Then FimInterv = FimInterv + 1
        End If
    Wend
    If Fim < FimInterv Then
        Fim = FimInterv
        Ret = Ret Or True
    End If
        
    AmpliarIntervaloLivre = Ret
End Function

Private Sub Class_Initialize()
    H = IsisSpaNew(AppHandle)
    ErroIniciacao = -1
    Set Msg = New ClMsg
End Sub

Private Sub Class_Terminate()
    Set Msg = Nothing
    IsisSpaDelete (H)
End Sub

'-----------------------------------------------------------------------
'IfIdentify  - identifica o arquivo invertido
'Nome   - nome do arquivo invertido
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function IfIdentify(ByVal Nome As String) As Boolean
    Dim Ret As Boolean
    Dim R As Long
    
    IfName = Nome
    R = IsisSpaIf(H, FullPathInv)
    If R = ZERO Then
        Ret = True
    Else
        Ret = False
    End If
    If Not Ret Then MsgBox "Erro em IfIdentify."
    IfIdentify = Ret
End Function

'-----------------------------------------------------------------------
'BDcopy     - copia a base de dados para uma nova base
'Destino    - nome do arquivo novo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function BDCopy(Destino As String) As Boolean
    Dim HDestino As Long
    Dim ctrl As IsisRecControl
    Dim Ret As Boolean
    Dim Mfn As Long
    Dim R As Long
            
    HDestino = IsisSpaNew(AppHandle)
    R = IsisSpaMf(HDestino, Destino)
    If IsisSpaMfCreate(HDestino) = ZERO Then
        If IsisRecControlMap(H, ctrl) > ZERO Then
            Ret = True
            While (Mfn < ctrl.nxtmfn - 1) And Ret
                Mfn = Mfn + 1
                If IsisRecRead(H, 0, Mfn) = ZERO Then
                    If IsisRecCopy(H, 0, HDestino, 0) = ZERO Then
                    'Msg.GiveRunInformation ("Mfn=" + CStr(Mfn))
                        Ret = (IsisRecWrite(HDestino, 0) = ZERO)
                    End If
                End If
            Wend
        End If
    End If
    IsisSpaDelete (HDestino)
    BDCopy = Ret
End Function

'-----------------------------------------------------------------------
'BDColetaLixo   - remove os Records vazios
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function BDColetaLixo() As Boolean
    Dim BDTEMP As ClIsisDll
    Dim Ret As Boolean
    Dim Mfn As Long
    Dim reg As String
    Dim q As Long
       
    Set BDTEMP = New ClIsisDll
    If BDTEMP.Inicia(Path, "bdtemp", "bdtemp", True) Then
        If BDTEMP.IfCreate(IfName) Then
            If BDCopy(Path + "\bdtemp") Then
                If BDDel Then
                    For Mfn = 1 To BDTEMP.MfnQuantity
                        reg = BDTEMP.RecordGet(Mfn)
                        If Len(reg) > 0 Then
                            RecordSave (reg)
                            q = q + 1
                        End If
                    Next
                End If
            End If
        End If
    End If
    Ret = (MfnQuantity = q) And (Mfn = BDTEMP.MfnQuantity)
    Set BDTEMP = Nothing
    Call DelFile(Path, "bdtemp.*")
    
    BDColetaLixo = Ret
End Function

'-----------------------------------------------------------------------
'BDDel  - apaga a base de dados
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function BDDel() As Boolean
    Dim Ret As Boolean
    
    If IsisSpaMf(H, FullPathBD) = ZERO Then
        Ret = (IsisSpaMfCreate(H) = ZERO)
    End If
    BDDel = Ret
End Function

Function RecordCopy(SourceMfn As Long, DestinyBD As ClIsisDll, DestinyMfn As Long) As Boolean
    Dim Ret As Boolean
    Dim registro As String
    
    'Obtenção do registro
    If (SourceMfn > 0) And (SourceMfn <= MfnQuantity) Then
        registro = RecordGet(SourceMfn)
    
        If DestinyMfn > 0 Then
            Ret = DestinyBD.RecordUpdate(DestinyMfn, registro)
        Else
            DestinyMfn = DestinyBD.RecordSave(registro)
            Ret = (DestinyMfn > 0)
        End If
    
        If Ret Then
            If Not DestinyBD.IfUpdate(DestinyMfn, DestinyMfn) Then
                Call Msg.GiveRunInformation("Failure updating " + DestinyBD.BDNome, True)
                Ret = False
            End If
        Else
            Call Msg.GiveRunInformation("Failure copying record.", True)
        End If
    End If
    RecordCopy = Ret
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
    Dim Ret As Boolean
    
    If Mfn > 0 Then
        If RecordUpdate(Mfn, Contents) Then
            Ret = IfUpdate(Mfn, Mfn)
        End If
    Else
        Mfn = RecordSave(Contents)
        If Mfn > 0 Then
            Ret = IfUpdate(Mfn, Mfn)
        End If
    End If
    Save = Ret
End Function

Public Function UsePft(Mfn As Long, format As String) As String
    Dim area As String * MaxTamArea
    Dim ResultLen As Long
    Dim result As String
    
    If IsisSpaMf(H, FullPathBD) = ZERO Then
        If IsisSpaPftCisis(H, format) = ZERO Then
            If IsisRecRead(H, 0, Mfn) = ZERO Then
                ResultLen = IsisRecFormatCisis(H, 0, area, MaxTamArea)
                If ResultLen > 0 Then result = Left(area, ResultLen)
            End If
        End If
    End If
    UsePft = result
End Function

Public Function UseProc(Mfn As Long, format As String) As Boolean
    Dim Ret As Boolean
    
    'If IsisSpaMf(H, FullPathBD) = ZERO Then
        If IsisRecRead(H, 0, Mfn) = ZERO Then
            If IsisRecFieldUpdate(H, 0, format) = ZERO Then
                If IsisRecWrite(H, 0) = ZERO Then Ret = True
            End If
        End If
    'End If
    UseProc = Ret
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
    Dim Occ As Long
    Dim Campo As Long
    Dim Max As Long
    Dim tam As Long
    Dim area As String * MaxTamArea
    
    If IsisRecRead(H, 0, Mfn) = ZERO Then
        Qtd = IsisRecNvf(H, 0)
        If Qtd > 0 Then
            ReDim pIsisRecDir(Qtd)
            ReDim Tags(Qtd)
            ReDim Occs(Qtd)
            ReDim Contents(Qtd)
            If IsisRecDirMap(H, 0, 1, Qtd, pIsisRecDir(0)) > ZERO Then
                For i = 1 To Qtd
                    Campo = pIsisRecDir(i - 1).tag
                    If Max < Campo Then
                        Max = Campo
                        ReDim Preserve done(Max)
                    End If
                    If Not done(Campo) Then
                        done(Campo) = True
                        QtdOcc = IsisRecFieldOcc(H, 0, Campo)
                        For Occ = 1 To QtdOcc
                            j = j + 1
                            tam = IsisRecField(H, 0, Campo, Occ, area, MaxTamArea)
                            Contents(j) = Left(area, tam)
                            Tags(j) = Campo
                            Occs(j) = Occ
                        Next
                    End If
                Next
            End If
        End If
    End If
    TagOccContentGet = Qtd
End Function

