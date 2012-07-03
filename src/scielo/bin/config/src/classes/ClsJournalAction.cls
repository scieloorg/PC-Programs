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
    
    fn = FreeFile
    Set journalList = journalDAO.getJournalStandardList
    Open Paths("Markup Issue Table").Path + "\journal-standard.txt" For Output As fn
    For i = 1 To journalList.count
        Set j = journalList(i)
        
        text = j.ISSN & "#" & j.shorttitle & "#" & j.JournalStandard & "#" & j.ISSNTYPE & "#" & j.CURRENTISSN & "#" & j.SUBJECT & "#" & j.MedlineTitle & "#" & j.pmid
        text = text & "#" & j.fulltitle & "#" & j.acron & "#" & j.print_issn & "#" & j.online_issn & "#" & j.publisherName
        
        Print #fn, text
    Next
    Close fn
End Sub

