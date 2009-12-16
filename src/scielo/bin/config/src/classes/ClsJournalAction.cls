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
    fn = FreeFile
    Set journalList = journalDAO.getJournalStandardList
    Open Paths("Markup Issue Table").path + "\journal-standard.txt" For Output As fn
    For i = 1 To journalList.count
        Print #fn, journalList(i).ISSN & "#" & journalList(i).ShortTitle & "#" & journalList(i).JournalStandard
    Next
    Close fn
End Sub

