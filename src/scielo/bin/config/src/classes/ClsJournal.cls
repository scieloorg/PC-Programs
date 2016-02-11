VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsJournal"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Public is_published As String

Public MedlineTitle As String
Public ISOTitle As String
Public parallelTitles As String
Public vocabulary As String
Public publisherName As String
Private mvarpubid As String

Private mvarJournalStatusHistory As ClsHistory
Private mvarJournalStandard As String
Private mvarISSN As String
Private mvarTitle As String
Private mvarKey As String
Private mvarShortTitle As String

Public CollectionURL As String
Private mvarSUBJECT As String
Public pmid As String

Public fulltitle As String
Public acron As String
Public print_issn As String
Public online_issn As String
Public license_code As String


Public Property Let SUBJECT(ByVal vNewValue As String)
    mvarSUBJECT = vNewValue
End Property

Public Property Get SUBJECT() As String
    SUBJECT = mvarSUBJECT
End Property
Public Property Get pubid() As Variant
    pubid = mvarpubid
End Property
Public Property Let pubid(ByVal vNewValue As Variant)
    mvarpubid = vNewValue
End Property
Public Property Get shorttitle() As Variant
    shorttitle = mvarShortTitle
End Property

Public Property Let shorttitle(ByVal vNewValue As Variant)
    mvarShortTitle = vNewValue
End Property
Public Property Get key() As Variant
    key = mvarKey
End Property
Public Property Let key(ByVal vNewValue As Variant)
    mvarKey = vNewValue
End Property
Public Property Get Title() As Variant
    Title = mvarTitle
End Property

Public Property Let Title(ByVal vNewValue As Variant)
    mvarTitle = vNewValue
End Property

Public Property Get ISSN() As Variant
    ISSN = mvarISSN
End Property

Public Property Let ISSN(ByVal vNewValue As Variant)
    mvarISSN = vNewValue
End Property
Public Property Get JournalStandard() As Variant
    JournalStandard = mvarJournalStandard
End Property

Public Property Let JournalStandard(ByVal vNewValue As Variant)
    mvarJournalStandard = vNewValue
End Property

Public Property Get journalStatusHistory() As Variant
    Set journalStatusHistory = mvarJournalStatusHistory
End Property

Public Property Set journalStatusHistory(ByVal vNewValue As Variant)
    Set mvarJournalStatusHistory = vNewValue
End Property
