VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsTOC_DAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private isisSection As ClIsisdll

Sub create(isis As ClIsisdll)
    Set isisSection = isis
End Sub
Private Function getTempHeader(Mfn As Long, language As String) As String
    Dim content As String
    
    content = isisSection.UsePft(Mfn, "(if v48^l='" + language + "' then v48^h fi)")
    getTempHeader = content
End Function

Private Sub getSections(Mfn As Long, lang As String, sections As ClsSections)
    Dim ITEMS() As String
    Dim texts() As String
    Dim i As Long
    
    Dim s As String
    
    Dim sectionObj As ClsSection
    Dim pairSectionTitleAndLang As ClsTextByLang
    
    Dim textSectionCode As String
    Dim textSectionTitle As String
    
    s = isisSection.UsePft(Mfn, "(if v49^l='" + lang + "' then v49^c|<CODE-TITLE-SEP>|,v49^t|<NEXTITEM>| fi)")
    ITEMS = Split(s, "<NEXTITEM>")
    
    For i = 0 To UBound(ITEMS) - 1
        texts = Split(ITEMS(i), "<CODE-TITLE-SEP>")
        textSectionCode = texts(0)
        textSectionTitle = texts(1)
    
        Set sectionObj = sections.item(textSectionCode)
        
        If sectionObj Is Nothing Then
        
            Set sectionObj = New ClsSection
            
            sectionObj.sectionCode = textSectionCode
            Set sectionObj.sectionNames = New ColTextByLang
            
            Set pairSectionTitleAndLang = New ClsTextByLang
            pairSectionTitleAndLang.lang = lang
            pairSectionTitleAndLang.text = textSectionTitle
            Call sectionObj.sectionNames.add(pairSectionTitleAndLang)
            
            Call sections.add(sectionObj, textSectionCode)
        Else
            Set pairSectionTitleAndLang = sectionObj.sectionNames.getItemByLang(lang)
            
            If pairSectionTitleAndLang Is Nothing Then
                Set pairSectionTitleAndLang = New ClsTextByLang
                pairSectionTitleAndLang.lang = lang
                pairSectionTitleAndLang.text = textSectionTitle
                Call sectionObj.sectionNames.add(pairSectionTitleAndLang)
            Else
                pairSectionTitleAndLang.text = textSectionTitle
                
            End If
        End If
    Next
    
        
End Sub

Function getTOC(mfnSection As Long, tocObj As ClsTOC) As ClsTOC
    
    Dim headers As ClsTextByLang
    Dim i As Long
    
       Set tocObj.sections = New ClsSections
        Set tocObj.names = New ColTextByLang
            
        For i = 1 To idiomsinfo.count
        
       
            Set headers = New ClsTextByLang
            headers.lang = idiomsinfo(i).Code
            
            If mfnSection > 0 Then
                headers.text = getTempHeader(mfnSection, idiomsinfo(i).Code)
                Call getSections(mfnSection, idiomsinfo(i).Code, tocObj.sections)
            End If
            If Len(headers.text) = 0 Then headers.text = idiomsinfo(i).More
            Call tocObj.names.add(headers)
            
        Next
    
    Set getTOC = tocObj
    
End Function


Function tagTOC(tocObj As ClsTOC) As String
    Dim ToCRecord As String
    
    Dim i As Long
    Dim j As Long
    
    If tocObj Is Nothing Then
    
    Else
    For i = 1 To tocObj.names.count
        With tocObj.names.getItemByIndex(i)
        ToCRecord = ToCRecord + TagContent("^l" + .lang + "^h" + .text, 48)
        End With
    Next
    
    For i = 1 To tocObj.sections.count
        With tocObj.sections.item(i)
            For j = 1 To .sectionNames.count
                If Len(.sectionNames.getItemByIndex(j).text) > 0 Then
                    ToCRecord = ToCRecord + TagContent("^l" + .sectionNames.getItemByIndex(j).lang + "^c" + .sectionCode + "^t" + .sectionNames.getItemByIndex(j).text, 49)
                End If
            Next
        End With
    Next
    End If
    tagTOC = ToCRecord
End Function
