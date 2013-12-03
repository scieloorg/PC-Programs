VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsJournalAction"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Sub generateJournalStandardListForMarkup()
    Dim journalList As MyCollection
    Dim i As Long
    Dim fn As Long
    Dim j As ClsJournal
    Dim text As String
    Dim Msg As String
    Dim msg2 As String
    Dim msg3 As String
    
    fn = FreeFile
    Set journalList = journalDAO.getJournalStandardList
    Open Paths("Markup Issue Table").Path + "\journal-standard.txt" For Output As fn
    For i = 1 To journalList.count
        Set j = journalList(i)
        If Len(j.fulltitle) > 0 And j.is_published = "C" Then
            Msg = j.fulltitle
                
            If Len(j.ISSN) <> 9 Then
                Msg = Msg & vbCrLf & " - Invalid ISSN " & j.ISSN
            End If
            If Len(j.shorttitle) = 0 Then
                Msg = Msg & vbCrLf & " - Missing short title."
            End If
            If Len(j.SUBJECT) = 0 Then
                Msg = Msg & vbCrLf & " - Missing subjects."
            End If
            If Len(j.acron) = 0 Then
                Msg = Msg & vbCrLf & " - Missing acron."
            End If
            If Len(j.publisherName) = 0 Then
                Msg = Msg & vbCrLf & " - Missing publisher name."
            End If
            
            If Len(j.JournalStandard) = 0 Then
                Msg = Msg & vbCrLf & " - Missing journal standard."
            End If
                
            If Len(Msg) > Len(j.fulltitle) Then
                msg2 = msg2 & vbCrLf & j.fulltitle
                msg3 = msg3 & vbCrLf & Msg
            Else
                text = j.ISSN & "#" & j.shorttitle & "#" & j.JournalStandard & "#" & "#" & "#" & j.SUBJECT & "#" & j.MedlineTitle & "#" & j.pmid
                text = text & "#" & j.fulltitle & "#" & j.acron & "#" & j.print_issn & "#" & j.online_issn & "#" & j.publisherName
                Print #fn, text
            End If
        End If
    Next
    Close fn
    
    If Len(msg2) > 0 Then
        MsgBox "Some journals data are incompleted. If you will use Markup Program for these journals, you have to complete the data, otherwise Markup will require " & Paths("Markup Issue Table").Path + "\journal-standard.txt" & vbCrLf & msg2
        MsgBox msg3
    End If
    
End Sub

