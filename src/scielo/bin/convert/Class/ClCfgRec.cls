VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClCfgRec"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'Store the Configuration Record
Private TMPCfgRec As ClIsisDll
Private CfgRecMfn As Long
Private DocMfn As Long
Private CfgRecDocDBPath As String
Private CfgRecDocDBName As String
Private mvarDocCounter As Long

Property Get DocCounter() As Long
    DocCounter = mvarDocCounter
End Property

Private Property Let DocCounter(Count As Long)
    mvarDocCounter = Count
End Property

Property Get CfgRecord() As String
    Set TMPCfgRec = New ClIsisDll
    If TMPCfgRec.Initiate(CfgRecDocDBPath, CfgRecDocDBName, "Doc DB") Then
        If CfgRecMfn > 0 Then CfgRecord = TMPCfgRec.RecordGet(CfgRecMfn)
    End If
    Set TMPCfgRec = Nothing
End Property

'----------------------------------------------------------------------
'CfgRecordSet  - Get issue record from the issue database or create it based on form data,
'                   and store it on <CfgRecord>
'CfgRecId    - the identification of the issue whose record will be gotten
'Return - <True> to sucess; <False> to failure
'----------------------------------------------------------------------
Function CfgRecordSet(CfgRecId As String) As Boolean
    
    Dim ret As Boolean
    Dim q As Long
    Dim CfgRecMfns() As Long
    Dim CfgRecDB  As ClIsisDll
    Dim counter As String
    Dim CfgRecord As String
    Dim i As Long
    Dim Item As ClCfgTag
    Dim item2 As ClPair
    Dim exist As Boolean
    
    CfgRecMfn = 0
    
    CfgRecDocDBPath = App.Path
    CfgRecDocDBName = "cfgrec"
    
    'Create the temporary configuration database
    Set TMPCfgRec = New ClIsisDll
    If TMPCfgRec.Initiate(CfgRecDocDBPath, CfgRecDocDBName, "Doc DB", True) Then
    
        If Len(BV(Currbv).Directory.ReturnCfgRecKey) > 0 Then
            'Get the configuration record from the configuration database
            If Len(CfgRecId) > 0 Then
                Set CfgRecDB = New ClIsisDll
                If CfgRecDB.Initiate(BV(Currbv).FileTree.DirNodes("Issue Database").fullpath, BV(Currbv).FileTree.DirNodes("Issue Database").text, BV(Currbv).FileTree.DirNodes("Issue Database").key) Then
                    If CfgRecDB.IfCreate(BV(Currbv).FileTree.DirNodes("Issue Database").text, BV(Currbv).FileTree.DirNodes("Issue Database").key) Then
                        q = CfgRecDB.MfnFind(CfgRecId, CfgRecMfns)
                        If q > 0 Then
                            CfgRecord = CfgRecDB.RecordGet(CfgRecMfns(q))
                        ElseIf q = 0 Then
                            Call Msg.GiveRunInformation(InterfaceLabels("MsgCfgRecMissingInCfgDB").elem2, True)
                        End If
                    End If
                End If
                Set CfgRecDB = Nothing
            End If
        Else
            'Create a configuration record based on the form data
            With BV(Currbv)
            For i = 1 To .Directory.Count
                Set Item = New ClCfgTag
                Set Item = .CfgTagCol(.Directory(i).LabDir, exist)
                If exist Then
                    Select Case Item.ContentType
                    Case "abbr"
                        CfgRecord = CfgRecord + TMPCfgRec.TagContents(.Directory(i).Value, Item.Tag)
                    Case "full"
                        Set item2 = New ClPair
                        Set item2 = .Directory(i).ContentListAbbr(.Directory(i).Value, exist)
                        If exist Then
                            CfgRecord = CfgRecord + TMPCfgRec.TagContents(item2.elem2, Item.Tag)
                        Else
                            CfgRecord = CfgRecord + TMPCfgRec.TagContents(.Directory(i).Value, Item.Tag)
                        End If
                    Case Else
                    
                    End Select
                End If
            Next
            End With
        End If
    End If
    
    'Insert the configuration record into the temporary configuration database
    If Len(CfgRecord) > 0 Then
        CfgRecMfn = TMPCfgRec.RecordSave(CfgRecord)
        If CfgRecMfn > 0 Then
            ret = True
            counter = TMPCfgRec.UsePft(CfgRecMfn, "v122")
            If IsNumber(counter) Then DocCounter = CLng(counter)
        End If
    End If
    Set TMPCfgRec = Nothing
    CfgRecordSet = ret
End Function

'-----------------------------------------------------------------------
'CheckField   - verifica a configuração de um elemento
'Label  - nome dos valores
'DocTag    - DocTag do campo
'CfgRecMfn    - mfn da base de dados (registro de configuração)
'DocMfn - mfn do documento (registro do documento)
'Retorno - configuração correta ou não
'-----------------------------------------------------------------------
Private Function CheckField(Label As String, DocTag As String, CfgRecTag As String, compare_tp As String) As Boolean
    Dim ret As Boolean
    Dim FromDoc As String
    Dim FromConfigRecord As String
    
    With TMPCfgRec
    
    FromDoc = .UsePft(DocMfn, DocTag)
    FromConfigRecord = .UsePft(CfgRecMfn, CfgRecTag)
        
    Select Case compare_tp
    Case "1"
        If StrComp(Replace(FromConfigRecord, Chr(160), Chr(32)), Replace(FromDoc, Chr(160), Chr(32)), vbBinaryCompare) = 0 Then
            ret = True
        Else
            If Len(FromConfigRecord) = 0 Then
                Call Msg.GiveRunInformation(InterfaceLabels(Label).elem2 + " " + InterfaceLabels("MsgMissingInCfgRec").elem2)
            Else
                Call Msg.GiveRunInformation(InterfaceLabels(Label).elem2 + " " + InterfaceLabels("MsgAsPresentInCfgRec").elem2 + FromConfigRecord + ".")
            End If
    
            If Len(FromDoc) = 0 Then
                Call Msg.GiveRunInformation(InterfaceLabels(Label).elem2 + " " + InterfaceLabels("MsgMissingInDoc").elem2)
            Else
                Call Msg.GiveRunInformation(InterfaceLabels(Label).elem2 + " " + InterfaceLabels("MsgAsPresentInDoc").elem2 + FromDoc + ".")
            End If
        End If
    Case "2"
        If StrComp(FromDoc, "nd", vbBinaryCompare) = 0 Then
            ret = True
        ElseIf InStr(FromConfigRecord, FromDoc + ";") > 0 Then
            ret = True
        End If
    Case "3"
        If FromConfigRecord Like String(4, "#") Then
            If InStr(FromDoc, FromConfigRecord) = 1 Then
                ret = True
            End If
        End If
    End Select
    End With
    If Not ret Then Call Msg.GiveRunInformation(FromDoc + " " + InterfaceLabels("MsgInvalidValue").elem2 + " " + InterfaceLabels(Label).elem2)
    CheckField = ret
End Function


'-----------------------------------------------------------------------
'CfgRecCheck - compara os registros de configuração do issue e do documento
'DocConfigRecord    - INPUT, registro de configuração do documento
'Retorno - <True> para configuração correta, <False> caso contrário
'-----------------------------------------------------------------------
Function CfgRecCheck(DocConfigRecord As String) As Boolean
    Dim ret As Boolean
    Dim i As Long
    
    Call Msg.GiveRunInformation(InterfaceLabels("MsgCheckingCfgDoc").elem2)
    
    Set TMPCfgRec = New ClIsisDll
    If TMPCfgRec.Initiate(CfgRecDocDBPath, CfgRecDocDBName, "Doc DB") Then
        If DocMfn = 0 Then
            DocMfn = TMPCfgRec.RecordSave(DocConfigRecord)
        Else
            If Not TMPCfgRec.RecordUpdate(DocMfn, DocConfigRecord) Then
                DocMfn = 0
            End If
        End If
    End If
        
    If (CfgRecMfn > 0) And (DocMfn > 0) Then
        
        ret = True
        For i = 1 To BV(Currbv).CfgTagCol.Count
            With BV(Currbv).CfgTagCol(i)
            ret = ret And CheckField(.LabelKey, .DocFieldPft, .CfgFieldPft, .CompareType)
            End With
        Next
        
    Else
        ret = True
    End If
    Set TMPCfgRec = Nothing
    
    CfgRecCheck = ret
End Function

'-----------------------------------------------------------------------
'ReturnDocId - compara os registros de configuração do issue e do documento
'DocConfigRecord    - INPUT, registro de configuração do documento
'Retorno - <True> para configuração correta, <False> caso contrário
'-----------------------------------------------------------------------
Function ReturnDocId(pft As String) As String
    Dim ret As String
    
    If Len(pft) > 0 Then
        Set TMPCfgRec = New ClIsisDll
        If TMPCfgRec.Initiate(CfgRecDocDBPath, CfgRecDocDBName, "Doc DB") Then
            If (DocMfn > 0) Then
                ret = TMPCfgRec.UsePft(DocMfn, pft)
            End If
        End If
        Set TMPCfgRec = Nothing
    End If
    ReturnDocId = ret
End Function

Private Sub Class_Terminate()
    Kill CfgRecDocDBPath + PathSep + CfgRecDocDBName + ".*"
End Sub

'----------------------------------------------------------------------
'ImportDocRecordContent  - Get issue record from the issue database and store it on <CfgRecord>
'CfgRecId    - the identification of the issue whose record will be gotten
'Return - <True> to sucess; <False> to failure
'----------------------------------------------------------------------
Function ImportDocRecordContent(pft As String) As String
    Dim content As String
    
    Set TMPCfgRec = New ClIsisDll
    If TMPCfgRec.Initiate(CfgRecDocDBPath, CfgRecDocDBName, "Doc DB") Then
        If DocMfn > 0 Then content = TMPCfgRec.UsePft(DocMfn, pft)
    End If
    Set TMPCfgRec = Nothing
            
    ImportDocRecordContent = content
End Function
