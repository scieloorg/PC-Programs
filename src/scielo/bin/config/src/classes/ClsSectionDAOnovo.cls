VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsSectionDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private isisSection As ClIsisdll
Public generalTOC_DAO As New ClsTOC_DAO
'


Sub create(Path As String, FileName As String, key As String)
    Set isisSection = New ClIsisdll
    If isisSection.Inicia(Path, FileName, key) Then
        If isisSection.IfCreate(FileName) Then
            Call generalTOC_DAO.create(isisSection)
        End If
    End If
End Sub

Public Function getTOC(SERIALTITLE As String, journalKey As String, pubid As String, mfn As Long) As ClsTOC
    
    Dim toc As New ClsTOC
    mfn = getRecordMfn(SERIALTITLE, journalKey, pubid)
    Set getTOC = generalTOC_DAO.getTOC(mfn, toc)
End Function

Private Function getRecordMfn(SerialTitle_to_find As String, journalKey As String, pubid As String) As Long
    Dim mfn As Long
    Dim SERIALTITLE As String
    Dim SerialISSN As String
    Dim found As Boolean
    Dim i As Long
    Dim MfnCounter As Long
    Dim SerialMfns() As Long
    
    
    'procura pela chave=ISSN
    MfnCounter = isisSection.MfnFind(journalKey, SerialMfns)
    i = 0
    While (i < MfnCounter) And (Not found)
        i = i + 1
        SERIALTITLE = isisSection.UsePft(SerialMfns(i), "v35")
        If StrComp(SERIALTITLE, journalKey) = 0 Then
            mfn = SerialMfns(i)
            found = True
        End If
    Wend
    
    'procura pela chave=titulo e pelo campo=título
    If Not found Then
        MfnCounter = isisSection.MfnFind(SerialTitle_to_find, SerialMfns)
        i = 0
        While (i < MfnCounter) And (Not found)
            i = i + 1
            'procura campo=title
            SERIALTITLE = isisSection.UsePft(SerialMfns(i), "v100")
            If StrComp(SERIALTITLE, SerialTitle_to_find) = 0 Then
                found = True
                mfn = SerialMfns(i)
            Else
                'procura campo=issn
                SerialISSN = isisSection.UsePft(SerialMfns(i), "v35")
                If StrComp(SerialISSN, journalKey) = 0 Then
                    found = True
                    mfn = SerialMfns(i)
                End If
            End If
        Wend
    End If
    

    If Not found Then
        mfn = 0
        While (mfn < isisSection.MfnQuantity) And (Not found)
            mfn = mfn + 1
            SERIALTITLE = isisSection.UsePft(mfn, "v930")
            If StrComp(SERIALTITLE, pubid) = 0 Then
                found = True
            End If
        Wend
    End If
    If found Then
        getRecordMfn = mfn
    End If

End Function
Function save(journalInfo As ClsJournal, toc As ClsTOC, Optional mfnSection As Long) As Boolean
    Dim s As String
    
    s = s + TagContent(getDateIso(Date), 91)
    s = s + TagContent(journalInfo.Title, 100)
    s = s + TagContent(journalInfo.shorttitle, 150)
    s = s + TagContent(journalInfo.issn, 35)
    s = s + TagContent(journalInfo.pubid, 930)
    s = s + generalTOC_DAO.tagTOC(toc)
        
    If mfnSection > 0 Then
        If isisSection.RecordUpdate(mfnSection, s) Then
            Call isisSection.IfUpdate(mfnSection, mfnSection)
        End If
    Else
        mfnSection = isisSection.RecordSave(s)
        If mfnSection > 0 Then Call isisSection.IfUpdate(mfnSection, mfnSection)
    End If
    save = (mfnSection > 0)
End Function
