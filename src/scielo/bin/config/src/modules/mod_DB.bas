Attribute VB_Name = "ModDB"
Option Explicit


Public journalDAO As ClsJournalDAO
Public journalAction As New ClsJournalAction
Public jlist As ClsJournalList
Const changelinetextbox = vbCrLf

Sub Serial_GetExisting(list As ListBox)
    Dim i As Long
    Dim current_status As String
    Dim publication_status As String
    On Error GoTo handle_error
    list.Clear
    Set jlist = journalDAO.getJournalList()
    
    For i = 1 To jlist.count
        current_status = jlist.getItemByIndex(i).journalStatusHistory.current_status
        publication_status = jlist.getItemByIndex(i).is_published
        
        If publication_status = "" Or current_status = "" Then
            current_status = ""
        ElseIf publication_status <> "C" Then
            current_status = codeStatus.item(publication_status).value
        ElseIf current_status <> "C" Then
            current_status = codeHistory.item(current_status).value
        Else
            current_status = ""
        End If
        If current_status <> "" Then
            current_status = "* (" + current_status + ") "
        Else
            current_status = "  "
        End If
        list.AddItem current_status + jlist.getItemByIndex(i).Title + " [" + jlist.getItemByIndex(i).ISSN + "]" ' + " (" + codeStatus.item(jlist.getItemByIndex(i).is_published) + ")"
    Next
    Exit Sub
handle_error:
    Debug.Print i
End Sub


Function Serial_CheckExisting(SerialTitle_to_find As String) As Long
    Dim journalKey As String
    Dim p As Long
    p = InStr(SerialTitle_to_find, "[")
    
    If p > 0 Then
        journalKey = Mid(SerialTitle_to_find, p + 1)
        journalKey = Mid(journalKey, 1, 9)
        Serial_CheckExisting = journalDAO.return_mfn_by_ISSN(journalKey)
    Else
        Serial_CheckExisting = journalDAO.return_mfn_by_title(SerialTitle_to_find)
    End If
End Function

Function Serial_TxtContent(Mfn As Long, tag As Long, Optional language As String) As String
'xxx
    Serial_TxtContent = journalDAO.getFieldContentByLanguage(Mfn, tag, language)
End Function

Function Serial_ComboDefaultValue(Code As ColCode, DefaultOption As String) As String
    Dim exist As Boolean
    Dim itemCode As ClCode
    Dim content As String
    
    
        If Len(DefaultOption) > 0 Then
            Set itemCode = New ClCode
            Set itemCode = Code(DefaultOption, exist)
            If exist Then
                content = itemCode.value
            Else
            Debug.Print
            End If
        End If
    
    Serial_ComboDefaultValue = content
End Function
Function Serial_ComboContent(Code As ColCode, Mfn As Long, tag As Long, Optional DefaultOption As String) As String
    Serial_ComboContent = journalDAO.getDecodedValue(Code, Mfn, tag, DefaultOption)
End Function

Function TagTxtContent(content As String, tag As Long) As String
    Dim p2 As Long
    Dim NewContent As String
    Dim p1 As Long
    
        content = content + changelinetextbox
        p1 = InStr(content, changelinetextbox)
        p2 = 1
        While p1 > 0
            NewContent = NewContent + TagContent(Mid(content, p2, p1 - p2), tag)
            p2 = p1 + Len(changelinetextbox)
            p1 = InStr(p2 + Len(changelinetextbox), content, changelinetextbox)
        Wend
    TagTxtContent = NewContent
End Function
Sub serial_issn_get(Mfn As Long, ByRef pissn As String, ByRef eissn As String)
    Dim v435 As String
    Dim v35 As String
    Dim v935 As String
    Dim v400 As String
    Dim issns() As String
    Dim issn_type() As String
    Dim i As Long
    
    pissn = ""
    eissn = ""
    v435 = journalDAO.getRepetitiveFieldValue(Mfn, 435, "%")
    If Len(v435) = 0 Then
        v35 = journalDAO.getRepetitiveFieldValue(Mfn, 35, "")
        v935 = journalDAO.getRepetitiveFieldValue(Mfn, 935, "")
        v400 = journalDAO.getRepetitiveFieldValue(Mfn, 400, "")
        If v35 = "ONLIN" Then
            eissn = v935
            If v935 <> v400 Then
                pissn = v400
            End If
        Else
            pissn = v935
            If v935 <> v400 Then
                eissn = v400
            End If
        End If
    Else
        issns = Split(v435, "%")
        For i = 0 To UBound(issns)
            If Len(issns(i)) > 0 Then
                issn_type = Split(issns(i), "^t")
                If issn_type(1) = "ONLIN" Then
                    eissn = issn_type(0)
                Else
                    pissn = issn_type(0)
                End If
            End If
        Next
    End If
End Sub
Sub serial_issn_build_field(ByRef pissn As String, ByRef eissn As String, ByRef v435 As String, ByRef v35 As String, ByRef v935 As String)
    v435 = ""
    If Len(pissn) > 0 Then
        v435 = pissn + "^tPRINT"
        v35 = "PRINT"
        v935 = pissn
    End If
    If Len(eissn) > 0 Then
        v435 = v435 + vbCrLf + eissn + "^tONLIN"
        v35 = "ONLIN"
        v935 = eissn
    End If
End Sub
Sub Serial_ListContent(list As ListBox, Code As ColCode, Mfn As Long, tag As Long)
    Dim content As String
    Dim exist As Boolean
    Dim itemCode As ClCode
    Dim sep As String
    Dim p As Long
    Dim item As String
    Dim i As Long
    Dim found As Boolean
    
    sep = "%"
    content = journalDAO.getRepetitiveFieldValue(Mfn, tag, sep)
    
    For i = 0 To list.ListCount - 1
        list.selected(i) = False
    Next
            
    Set itemCode = New ClCode
    
    p = InStr(content, sep)
    While p > 0
        item = Mid(content, 1, p - 1)
        Set itemCode = Code(item, exist)
        If exist Then
            item = itemCode.value
            i = 0
            found = False
            While (i < list.ListCount) And (Not found)
                If StrComp(item, list.list(i), vbTextCompare) = 0 Then
                    found = True
                    list.selected(i) = True
                End If
                i = i + 1
            Wend
        Else
            
        End If
        content = Mid(content, p + 1)
        p = InStr(content, sep)
    Wend
End Sub



Function Serial_Save(MfnTitle As Long) As Long
    Dim reccontent As String
    Dim i As Long
    Dim msgwarning As String
    Dim OK As Boolean
            
        reccontent = reccontent + TagTxtContent(Serial1.TxtISSN.text, 400)
        reccontent = reccontent + TagTxtContent(Serial1.TxtSerTitle.text, 100)
        reccontent = reccontent + TagTxtContent(Serial1.TxtSubtitle.text, 110)
        reccontent = reccontent + TagTxtContent(Serial1.TxtShortTitle.text, 150)
        reccontent = reccontent + TagTxtContent(Serial1.TxtISOStitle.text, 151)
        reccontent = reccontent + TagTxtContent(Serial1.TxtSectionTitle.text, 130)
        reccontent = reccontent + TagTxtContent(Serial1.TxtParallel.text, 230)
        reccontent = reccontent + TagTxtContent(Serial1.TxtOthTitle.text, 240)
        reccontent = reccontent + TagTxtContent(Serial1.TxtOldTitle.text, 610)
        reccontent = reccontent + TagTxtContent(Serial1.TxtNewTitle.text, 710)
        reccontent = reccontent + TagTxtContent(Serial1.TxtIsSuppl.text, 560)
        reccontent = reccontent + TagTxtContent(Serial1.TxtHasSuppl.text, 550)
        
        
        For i = 1 To idiomsinfo.count
            If Len(Serial2.TxtMission(i).text) > 0 Then reccontent = reccontent + TagTxtContent(Serial2.TxtMission(i).text + "^l" + idiomsinfo(i).Code, 901)
        Next
        
        reccontent = reccontent + TagTxtContent(UCase(Serial2.TxtDescriptors.text), 440)
        reccontent = reccontent + TagListContent(CodeStudyArea, Serial2.ListStudyArea, 441)
        reccontent = reccontent + TagListContent(wok_subjects, Serial2.List_wok_area, 854)
        
        If Serial2.check_wok_scie.value = 1 Then
            reccontent = reccontent + TagTxtContent("SCIE", 851)
        End If
        If Serial2.check_wok_ssci.value = 1 Then
            reccontent = reccontent + TagTxtContent("SSCI", 852)
        End If
        If Serial2.check_wok_aehci.value = 1 Then
            reccontent = reccontent + TagTxtContent("A&HCI", 853)
        End If
        reccontent = reccontent + TagTxtContent(Serial2.TxtIdxRange.text, 450)
        
        reccontent = reccontent + TagComboContent(CodeLiteratureType, Serial3.ComboTpLit.text, 5)
        reccontent = reccontent + TagComboContent(CodeTreatLevel, Serial3.ComboTreatLev.text, 6)
        reccontent = reccontent + TagComboContent(CodePubLevel, Serial3.ComboPubLev.text, 330)
            
        reccontent = reccontent + TagTxtContent(Serial3.TxtInitDate.text, 301)
        reccontent = reccontent + TagTxtContent(Serial3.TxtInitVol.text, 302)
        reccontent = reccontent + TagTxtContent(Serial3.TxtInitNo.text, 303)
        reccontent = reccontent + TagTxtContent(Serial3.TxtTermDate.text, 304)
        reccontent = reccontent + TagTxtContent(Serial3.TxtFinVol.text, 305)
        reccontent = reccontent + TagTxtContent(Serial3.TxtFinNo.text, 306)
            
        reccontent = reccontent + TagComboContent(CodeFrequency, Serial3.ComboFreq.text, 380)
        reccontent = reccontent + TagComboContent(codeStatus, Serial3.ComboPubStatus.text, 50)
        reccontent = reccontent + TagComboContent(CodeAlphabet, Serial3.ComboAlphabet.text, 340)
        reccontent = reccontent + TagListContent(CodeTxtLanguage, Serial3.ListTextIdiom, 350)
        reccontent = reccontent + TagListContent(CodeAbstLanguage, Serial3.ListAbstIdiom, 360)
            
        reccontent = reccontent + TagTxtContent(Serial3.TxtNationalcode.text, 20)
        reccontent = reccontent + TagTxtContent(Serial3.TxtClassif.text, 430)
        reccontent = reccontent + TagComboContent(CodeStandard, Serial3.ComboStandard.text, 117)
        reccontent = reccontent + TagListContent(CodeScheme, Serial3.ListScheme, 85)
        
        reccontent = reccontent + TagTxtContent(Serial4.TxtPublisher.text, 480)
        
        reccontent = reccontent + TagComboContent(CodeCountry, Serial4.ComboCountry.text, 310)
        reccontent = reccontent + TagComboContent(CodeState, Serial4.ComboState.text, 320)
        'reccontent = reccontent + TagTxtContent(Serial3.TxtPubState.Text, 320)
        
        reccontent = reccontent + TagTxtContent(Serial4.TxtPubCity.text, 490)
            
        reccontent = reccontent + TagTxtContent(Serial4.TxtAddress.text, 63)
        reccontent = reccontent + TagTxtContent(Serial4.TxtPhone.text, 631)
        reccontent = reccontent + TagTxtContent(Serial4.TxtFaxNumber.text, 632)
        reccontent = reccontent + TagTxtContent(Serial4.TxtEmail.text, 64)
        reccontent = reccontent + TagTxtContent(JOURNAL5.TxtCprightDate.text, 621)
        reccontent = reccontent + TagTxtContent(JOURNAL5.TxtCprighter.text, 62)
        reccontent = reccontent + TagTxtContent(Serial4.TxtSponsor.text, 140)
            
        reccontent = reccontent + TagTxtContent(Serial3.TxtSECS.text, 37)
        reccontent = reccontent + TagTxtContent(Serial3.TxtMEDLINE.text, 420)
        reccontent = reccontent + TagTxtContent(Serial3.TxtMEDLINEStitle.text, 421)
        reccontent = reccontent + TagTxtContent(SERIAL8.TxtNotes.text, 900)
        
        reccontent = reccontent + TagTxtContent(SERIAL7.TxtSiglum.text, 930)
        reccontent = reccontent + TagTxtContent(SERIAL7.TxtPubId.text, 68)
        reccontent = reccontent + TagTxtContent(SERIAL7.TxtSep.text, 65)
        reccontent = reccontent + TagTxtContent(SERIAL7.TxtSiteLocation.text, 69)
        reccontent = reccontent + TagComboContent(CodeFTP, SERIAL7.ComboFTP.text, 66)
        
        Dim v435 As String
        Dim v35 As String
        Dim v935 As String
        
        Call serial_issn_build_field(SERIAL7.Text_PISSN.text, SERIAL7.Text_EISSN.text, v435, v35, v935)
        reccontent = reccontent + TagTxtContent(v435, 435)
        reccontent = reccontent + TagTxtContent(v935, 935)
        reccontent = reccontent + TagTxtContent(v35, 35)
        
        reccontent = reccontent + TagComboContent(CodePublishingModel, SERIAL7.ComboPublishingModel.text, 699)
        reccontent = reccontent + TagComboContent(CodeUsersubscription, SERIAL7.ComboUserSubscription.text, 67)
        reccontent = reccontent + TagTxtContent(SERIAL7.Text1.text, 690)
        reccontent = reccontent + TagTxtContent(SERIAL7.ScieloNetWrite, 691)
        reccontent = reccontent + TagTxtContent(SERIAL7.Text_SubmissionOnline.text, 692)
        
        
        reccontent = reccontent + TagComboContent(CodeCCode, SERIAL8.ComboCCode.text, 10)
        reccontent = reccontent + TagTxtContent(SERIAL8.TxtIdNumber.text, 30)
        reccontent = reccontent + TagTxtContent(SERIAL8.TxtDocCreation.text, 950)
        reccontent = reccontent + TagTxtContent(SERIAL8.TxtCreatDate.text, 940)
        reccontent = reccontent + TagTxtContent(SERIAL8.TxtDocUpdate.text, 951)
        
        SERIAL8.TxtUpdateDate.text = getDateIso(Date)
        reccontent = reccontent + TagTxtContent(SERIAL8.TxtUpdateDate.text, 941)
        reccontent = reccontent + SERIAL6.getDataToSave
        reccontent = reccontent + TagTxtContent(JOURNAL5.ComboLicText.text, 541)
        
        If MfnTitle = 0 Then
            If journalDAO.return_mfn_by_ISSN(Serial1.TxtISSN.text) > 0 Then
            
            Else
                Call journalDAO.save(MfnTitle, reccontent)
            End If
        Else
            Call journalDAO.save(MfnTitle, reccontent)
        End If
    Serial_Save = MfnTitle
End Function

Function TagComboContent(Code As ColCode, content As String, tag As Long) As String
    Dim exist As Boolean
    Dim itemCode As ClCode
        
    If Len(content) > 0 Then
        Set itemCode = New ClCode
        Set itemCode = Code(content, exist)
        If exist Then
            content = itemCode.Code
        Else
        
        End If
    End If
    TagComboContent = TagContent(content, tag)
End Function

Function TagListContent(Code As ColCode, list As ListBox, tag As Long) As String
    Dim exist As Boolean
    Dim itemCode As ClCode
    Dim i As Long
    Dim content As String
    
        Set itemCode = New ClCode
        For i = 0 To list.ListCount - 1
            If list.selected(i) Then
                Set itemCode = Code(list.list(i), exist)
                If exist Then
                    content = content + TagContent(itemCode.Code, tag)
                Else
                    Debug.Print
                End If
            End If
        Next
            
    TagListContent = content
End Function

Sub FillListStudyArea(list As ListBox, Code As ColCode)
    Dim i As Long
    
    list.Clear
    For i = 1 To Code.count
        If StrComp(Code(i).value, Code(i).Code) = 0 Then
            list.AddItem Code(i).value
        Else
            If (i Mod 2) <> 0 Then
                list.AddItem Code(i).value
            End If
        End If
    Next
End Sub
Sub FillList(list As ListBox, Code As ColCode)
    Dim i As Long
    
    list.Clear
    
    For i = 1 To Code.count
        list.AddItem Code(i).value
    Next
End Sub

Sub FillCombo(combo As ComboBox, Code As ColCode, Optional valueEqCode As Boolean = False)
    Dim i As Long
    
    combo.Clear
    For i = 1 To Code.count
        If Not Code(i).unabled Then
            If valueEqCode Then
                combo.AddItem Code(i).Code
            Else
                combo.AddItem Code(i).value
            End If
        End If
    Next
End Sub

Sub UnselectList(list As ListBox)
    Dim i As Long
    
    For i = 0 To list.ListCount - 1
        list.selected(i) = False
    Next
End Sub

Sub UnloadSerialForms()
    Dim IsNewSerial As Boolean
    IsNewSerial = Serial1.FillingNewSerial
    Unload SERIAL8
    Unload SERIAL7
    Unload SERIAL6
    Unload JOURNAL5
    Unload Serial4
    Unload Serial3
    Unload Serial2
    Unload Serial1
    Unload FrmInfo
    journalAction.generateJournalStandardListForMarkup
    If IsNewSerial Then
        Call Serial_GetExisting(FrmNewSerial.ListExistingSerial)
        FrmNewSerial.Show
    Else
        FrmExistingSerial.Show
        Call Serial_GetExisting(FrmExistingSerial.ListExistingSerial)
    End If
End Sub
 
Function Serial_Close(MyMfnTitle As Long) As Integer
    Dim resp As VbMsgBoxResult
    Dim QClose As Integer
    Dim QExit As Boolean
    
    QExit = Not SERIAL6.WarnMandatoryFields
    
    If Not QExit Then
        If TitleCloseDenied Then
            MsgBox ConfigLabels.getLabel("MsgUnabledtoClose")
        Else
            resp = MsgBox(ConfigLabels.getLabel("MsgExit"), vbYesNo + vbDefaultButton2)
            If resp = vbYes Then
                QExit = True
            ElseIf resp = vbNo Then
                QExit = False
            End If
        End If
    End If
    
    If QExit Then
        If Serial_ChangedContents(MyMfnTitle) Then
            resp = MsgBox(ConfigLabels.getLabel("MsgSaveChanges"), vbYesNoCancel)
            If resp = vbCancel Then
            
            ElseIf resp = vbYes Then
                QClose = 2
            ElseIf resp = vbNo Then
                QClose = 1
            End If
        Else
            QClose = 1
        End If
    End If
    Serial_Close = QClose
End Function

Function Serial_ChangedContents(MfnTitle As Long) As Boolean
    Dim change As Boolean
    Dim i As Long
    Dim pissn As String
    Dim eissn As String
    
    change = (StrComp(Serial1.TxtISSN.text, Serial_TxtContent(MfnTitle, 400)) <> 0)
    change = change Or (StrComp(Serial1.TxtSerTitle.text, Serial_TxtContent(MfnTitle, 100)) <> 0)
    change = change Or (StrComp(Serial1.TxtSubtitle.text, Serial_TxtContent(MfnTitle, 110)) <> 0)
    change = change Or (StrComp(Serial1.TxtShortTitle.text, Serial_TxtContent(MfnTitle, 150)) <> 0)
    change = change Or (StrComp(Serial1.TxtISOStitle.text, Serial_TxtContent(MfnTitle, 151)) <> 0)
    change = change Or (StrComp(Serial1.TxtSectionTitle.text, Serial_TxtContent(MfnTitle, 130)) <> 0)
    change = change Or (StrComp(Serial1.TxtParallel.text, Serial_TxtContent(MfnTitle, 230)) <> 0)
    change = change Or (StrComp(Serial1.TxtOthTitle.text, Serial_TxtContent(MfnTitle, 240)) <> 0)
    change = change Or (StrComp(Serial1.TxtOldTitle.text, Serial_TxtContent(MfnTitle, 610)) <> 0)
    change = change Or (StrComp(Serial1.TxtNewTitle.text, Serial_TxtContent(MfnTitle, 710)) <> 0)
    change = change Or (StrComp(Serial1.TxtIsSuppl.text, Serial_TxtContent(MfnTitle, 560)) <> 0)
    change = change Or (StrComp(Serial1.TxtHasSuppl.text, Serial_TxtContent(MfnTitle, 550)) <> 0)
    
    For i = 1 To idiomsinfo.count
        change = change Or (StrComp(Serial2.TxtMission(i).text, Serial_TxtContent(MfnTitle, 901, idiomsinfo(i).Code)) <> 0)
    Next

    change = change Or (StrComp(Serial2.TxtDescriptors.text, Serial_TxtContent(MfnTitle, 440), vbTextCompare) <> 0)
    'change = change Or (StrComp(Serial2.ListStudyArea.Text, Serial_TxtContent(MfnTitle, 441)) <> 0)
    
    change = change Or Serial_ChangedListContent(Serial2.ListStudyArea, CodeStudyArea, MfnTitle, 441)
    change = change Or Serial_ChangedListContent(Serial2.List_wok_area, wok_subjects, MfnTitle, 854)

    change = change Or (StrComp(Serial3.ComboTpLit.text, Serial_ComboContent(CodeLiteratureType, MfnTitle, 5)) <> 0)
    change = change Or (StrComp(Serial3.ComboTreatLev.text, Serial_ComboContent(CodeTreatLevel, MfnTitle, 6)) <> 0)
    change = change Or (StrComp(Serial3.ComboPubLev.text, Serial_ComboContent(CodePubLevel, MfnTitle, 330)) <> 0)
    
    change = change Or is_changed(Serial2.check_wok_scie.value, Serial_TxtContent(MfnTitle, 851))
    change = change Or is_changed(Serial2.check_wok_ssci.value, Serial_TxtContent(MfnTitle, 852))
    change = change Or is_changed(Serial2.check_wok_aehci.value, Serial_TxtContent(MfnTitle, 853))
    
    change = change Or (StrComp(Serial3.TxtInitVol.text, Serial_TxtContent(MfnTitle, 302)) <> 0)
    change = change Or (StrComp(Serial3.TxtInitNo.text, Serial_TxtContent(MfnTitle, 303)) <> 0)
    change = change Or (StrComp(Serial3.TxtTermDate.text, Serial_TxtContent(MfnTitle, 304)) <> 0)
    change = change Or (StrComp(Serial3.TxtFinVol.text, Serial_TxtContent(MfnTitle, 305)) <> 0)
    change = change Or (StrComp(Serial3.TxtFinNo.text, Serial_TxtContent(MfnTitle, 306)) <> 0)
    
    change = change Or (StrComp(Serial3.ComboFreq.text, Serial_ComboContent(CodeFrequency, MfnTitle, 380)) <> 0)
    change = change Or (StrComp(Serial3.ComboPubStatus.text, Serial_ComboContent(codeStatus, MfnTitle, 50)) <> 0)
    change = change Or (StrComp(Serial3.ComboAlphabet.text, Serial_ComboContent(CodeAlphabet, MfnTitle, 340)) <> 0)
    change = change Or (StrComp(Serial3.ComboStandard.text, Serial_ComboContent(CodeStandard, MfnTitle, 117)) <> 0)
        
    change = change Or (StrComp(Serial3.TxtNationalcode.text, Serial_TxtContent(MfnTitle, 20)) <> 0)
    change = change Or (StrComp(Serial3.TxtClassif.text, Serial_TxtContent(MfnTitle, 430)) <> 0)
    change = change Or (StrComp(Serial4.TxtPublisher.text, Serial_TxtContent(MfnTitle, 480)) <> 0)
    change = change Or (StrComp(Serial4.ComboCountry.text, Serial_ComboContent(CodeCountry, MfnTitle, 310)) <> 0)
    change = change Or (StrComp(Serial4.ComboState.text, Serial_ComboContent(CodeState, MfnTitle, 320)) <> 0)
    'change = change Or (StrComp(Serial3.TxtPubState.Text, Serial_TxtContent(MfnTitle, 320)) <> 0)
    change = change Or (StrComp(Serial4.TxtPubCity.text, Serial_TxtContent(MfnTitle, 490)) <> 0)

    change = change Or (StrComp(Serial4.TxtAddress.text, Serial_TxtContent(MfnTitle, 63)) <> 0)
    change = change Or (StrComp(Serial4.TxtPhone.text, Serial_TxtContent(MfnTitle, 631)) <> 0)
    change = change Or (StrComp(Serial4.TxtFaxNumber.text, Serial_TxtContent(MfnTitle, 632)) <> 0)
    change = change Or (StrComp(Serial4.TxtEmail.text, Serial_TxtContent(MfnTitle, 64)) <> 0)
    
    change = change Or (StrComp(JOURNAL5.ComboLicText.text, Serial_TxtContent(MfnTitle, 541)) <> 0)
    change = change Or (StrComp(JOURNAL5.TxtCprightDate.text, Serial_TxtContent(MfnTitle, 621)) <> 0)
    change = change Or (StrComp(JOURNAL5.TxtCprighter.text, Serial_TxtContent(MfnTitle, 62)) <> 0)
    change = change Or (StrComp(Serial4.TxtSponsor.text, Serial_TxtContent(MfnTitle, 140)) <> 0)
    change = change Or (StrComp(Serial3.TxtSECS.text, Serial_TxtContent(MfnTitle, 37)) <> 0)
    change = change Or (StrComp(Serial3.TxtMEDLINE.text, Serial_TxtContent(MfnTitle, 420)) <> 0)
    change = change Or (StrComp(Serial3.TxtMEDLINEStitle.text, Serial_TxtContent(MfnTitle, 421)) <> 0)
    change = change Or (StrComp(Serial2.TxtIdxRange.text, Serial_TxtContent(MfnTitle, 450)) <> 0)
    change = change Or (StrComp(SERIAL8.TxtNotes.text, Serial_TxtContent(MfnTitle, 900)) <> 0)
    
    change = change Or (StrComp(SERIAL7.TxtSiglum.text, Serial_TxtContent(MfnTitle, 930)) <> 0)
    change = change Or (StrComp(SERIAL7.TxtPubId.text, Serial_TxtContent(MfnTitle, 68)) <> 0)
    change = change Or (StrComp(SERIAL7.TxtSep.text, Serial_TxtContent(MfnTitle, 65)) <> 0)
    change = change Or (StrComp(SERIAL7.TxtSiteLocation.text, Serial_TxtContent(MfnTitle, 69)) <> 0)
    change = change Or (StrComp(SERIAL7.ComboFTP.text, Serial_ComboContent(CodeFTP, MfnTitle, 66)) <> 0)
    
    Call serial_issn_get(MfnTitle, pissn, eissn)
    
    change = change Or (StrComp(SERIAL7.Text_PISSN.text, pissn) <> 0)
    change = change Or (StrComp(SERIAL7.Text_EISSN.text, eissn) <> 0)
    
    change = change Or (StrComp(SERIAL7.Text1.text, Serial_TxtContent(MfnTitle, 690)) <> 0)
    change = change Or (StrComp(SERIAL7.ComboUserSubscription.text, Serial_ComboContent(CodeUsersubscription, MfnTitle, 67)) <> 0)
    change = change Or (StrComp(SERIAL7.ComboPublishingModel.text, Serial_ComboContent(CodePublishingModel, MfnTitle, 699)) <> 0)
    change = change Or (StrComp(SERIAL7.Text_SubmissionOnline.text, Serial_TxtContent(MfnTitle, 692)) <> 0)
    
    change = change Or (StrComp(SERIAL8.ComboCCode.text, Serial_ComboContent(CodeCCode, MfnTitle, 10)) <> 0)
    Dim x As String
    Dim n As Long
    
    x = Serial_TxtContent(MfnTitle, 691)
    If Len(SERIAL7.ScieloNetWrite) > Len(x) Then
        n = Len(SERIAL7.ScieloNetWrite) - Len(x)
        x = x + Replace(Space(n), " ", "0")
    End If
    change = change Or (StrComp(SERIAL7.ScieloNetWrite, x) <> 0)
    change = change Or (StrComp(SERIAL8.TxtIdNumber.text, Serial_TxtContent(MfnTitle, 30)) <> 0)
    change = change Or (StrComp(SERIAL8.TxtDocUpdate.text, Serial_TxtContent(MfnTitle, 951)) <> 0)
    
    change = change Or Serial_ChangedListContent(Serial3.ListScheme, CodeScheme, MfnTitle, 85)
    change = change Or Serial_ChangedListContent(Serial3.ListTextIdiom, CodeTxtLanguage, MfnTitle, 350)
    change = change Or Serial_ChangedListContent(Serial3.ListAbstIdiom, CodeAbstLanguage, MfnTitle, 360)
    change = change Or SERIAL6.changed(MfnTitle)
    change = change Or JOURNAL5.changed(MfnTitle)
    
    Serial_ChangedContents = change
End Function

Function is_changed(value As Integer, db_value As String) As Boolean
    Dim v As Integer
    v = 0
    If Len(db_value) > 0 Then v = 1
    
    is_changed = (v <> value)
End Function
Function Serial_ChangedListContent(list As ListBox, Code As ColCode, MfnTitle As Long, tag As Long) As Boolean
    Dim content As String
    Dim exist As Boolean
    Dim changed As Long
    Dim itemCode As ClCode
    Dim sep As String
    Dim p As Long
    Dim item As String
    Dim i As Long
    Dim values As String
    
    sep = "%"
    
    content = journalDAO.getRepetitiveFieldValue(MfnTitle, tag, sep)
    
    Set itemCode = New ClCode
    p = InStr(content, sep)
    While p > 0
        item = Mid(content, 1, p - 1)
        Set itemCode = Code(item, exist)
        If exist Then values = values + itemCode.value + sep
        content = Mid(content, p + 1)
        p = InStr(content, sep)
    Wend
    values = sep + values
    
    For i = 0 To list.ListCount - 1
        If list.selected(i) Then
            'esta selecionado mas nao esta na base
            If InStr(values, sep + list.list(i) + sep) = 0 Then
                changed = changed + 1
            End If
        Else
            'nao esta selecionado mas esta na base
            If InStr(values, sep + list.list(i) + sep) > 0 Then
                changed = changed + 1
            End If
        End If
    Next
    
    Serial_ChangedListContent = (changed > 0)
    
End Function

Sub CancelFilling()
    Dim resp As VbMsgBoxResult
    
    resp = MsgBox(ConfigLabels.getLabel("MsgExit"), vbYesNo)
    If resp = vbYes Then
        UnloadSerialForms
    ElseIf resp = vbNo Then
    
    End If
End Sub

Sub FormQueryUnload(Cancel As Integer, UnloadMode As Integer)

    If UnloadMode = vbFormControlMenu Then
        Cancel = 1
        MsgBox ConfigLabels.getLabel("MsgClosebyCancelorClose")
    End If
End Sub

Function Serial_Remove(mfns() As Long, q As Long) As Boolean
    Dim i As Long
    For i = 1 To q
        journalDAO.delete (mfns(i))
    Next
End Function

Function getCode(Code As ColCode, content As String) As ClCode
    Dim exist As Boolean
    Dim itemCode As ClCode
    Dim r As ClCode
    
    If Len(content) > 0 Then
        
        Set itemCode = Code(content, exist)
        If exist Then
            Set r = itemCode
        End If
    End If
    
    Set getCode = r
End Function

Sub generateSciELOURL()
    Dim i As Long
    Dim fn As Long
    Dim defaultCollectionURL As String
    Dim curl As String
    
    fn = FreeFile
    Open Paths("SciELO URL").Path + "\" + Paths("SciELO URL").FileName For Output As fn
    
    defaultCollectionURL = Paths("SciELO WEB URL").FileName
    For i = 1 To jlist.count
        With jlist.getItemByIndex(i)
        If .CollectionURL <> "" Then
            curl = .CollectionURL
        Else
            curl = defaultCollectionURL
        End If
        Print #fn, .pubid & "|" & curl & "|" & .Title
        End With
    Next
    Close fn
End Sub
Sub generateFile_JournalList4Automata()
    Dim i As Long
    Dim fn As Long
    Dim defaultCollectionURL As String
    Dim curl As String
    
    Dim citat As ClsParams
    Dim c As String
    Dim tgs As New ClsParams
    Dim tg As String
    
    Set citat = New ClsParams
    For i = 1 To CodeStandard.count
        c = Mid(CodeStandard(i).Code, 1, 1)
        Select Case CodeStandard(i).Code
        Case "iso690"
            tg = "tgiso"
        Case "nbr6023"
            c = "a"
            tg = "tgabnt"
        Case "other"
            tg = "tgother"
        Case "vancouv"
            tg = "tgvanc"
        Case "apa"
            c = "p"
            tg = "tgapa"
        End Select
        
        Call citat.add(c, CodeStandard(i).Code)
        Call tgs.add(tg, CodeStandard(i).Code)
    Next
    
    fn = FreeFile
    Open Paths("JournalList4Automata").Path + "\" + Paths("JournalList4Automata").FileName For Output As fn
    ' Acta Cir. Bras.;ocitat;acb.amd;tgother.amd
    For i = 1 To jlist.count
        With jlist.getItemByIndex(i)
        Print #fn, .ISSN & ";" & citat.item(.JournalStandard) & "citat;" & .pubid & ".amd;" & tgs.item(.JournalStandard) & ".amd"
        Print #fn, ""
        End With
    Next
    Close fn
End Sub
Function isTitleFormCompleted(Mfn As Long) As Boolean
    Dim i As Long
    Dim Data As String
    Dim missing As String
    
    For i = 1 To Fields.getMandatoryFields.count
        Data = journalDAO.getRepetitiveFieldValue(Mfn, CLng(Fields.getMandatoryFields.item(i)), "")
        If Len(Data) = 0 Then
            missing = missing + vbCrLf + Fields.getMandatoryFields.item(i)
        End If
    Next
    
    isTitleFormCompleted = (Len(missing) = 0)
End Function
