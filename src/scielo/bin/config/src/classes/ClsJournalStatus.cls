VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsJournalStatus"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False



Private mvarStatusDate As String
Private mvarStatus As String

 Property Get status() As String
    status = mvarStatus
End Property

 Property Let status(ByVal vNewValue As String)
    mvarStatus = vNewValue
End Property
 Property Get statusDate() As String
    statusDate = mvarStatusDate
End Property

 Property Let statusDate(ByVal vNewValue As String)
    mvarStatusDate = vNewValue
End Property



