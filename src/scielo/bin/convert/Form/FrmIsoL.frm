VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   5265
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   8235
   LinkTopic       =   "Form1"
   ScaleHeight     =   5265
   ScaleWidth      =   8235
   StartUpPosition =   3  'Windows Default
   Begin VB.CommandButton Command1 
      Caption         =   "Command1"
      Height          =   735
      Left            =   1920
      TabIndex        =   0
      Top             =   3480
      Width           =   1695
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Command1_Click()

End Sub

Private Sub GenerateIsoList()
    Dim startdir As String
    Dim i As Long
    
    With BV(Currbv)
    
    startdir = .FileTree.DirNodes("Serial Directory").FullPath
    
    For i = 1 To .Directory.Count
        Select Case .Directory(i).ObjTypeDir
        Case "combo"
            .Directory(i).Value = .Directory(i).ContentListFull(ComboFolder(i).Text).elem2
        Case "text", "label"
            .Directory(i).Value = TxtFolder(i).Text
        End Select
        If .Directory(i).Value Like .Directory(i).pattern Then
            'inputdataOk = True
        Else
            Call Msg.GiveRunInformation(InterfaceLabels(.Directory(i).MsgInvalidData).elem2, True)
            inputdataOk = False
        End If
    Next
    
    If inputdataOk Then
        PathCurr = .FileTree.DirNodes("Serial Directory").FullPath + .Directory.ReturnDataPath + PathSep
        
        'Find/Create the files/database related to the selected issue to convert
        If SetSelectedDir(PathCurr, FileCounter) Then
            ListDoc.path = PathCurr + .FileTree.DirNodes("Markup Directory").Text
            LabDocCounter.Caption = InterfaceLabels("LabFileCount").elem2 + CStr(ListDoc.ListCount)
            CmdSelectAll_Click
            ViewSuccessAndFailure
            'Check the number of documents listed on the form and the number of documents previously  inserted in the issue database
            'If they are different, there must be an error in issue database or in the markup directory
            If Len(.Directory.ReturnCfgRecKey) > 0 Then
                If FileCounter = ListDoc.ListCount Then
                    
                    ret = True
                Else
                    Call Msg.GiveRunInformation(InterfaceLabels("MsgInvalidNumberofDoc").elem2 + vbCrLf + InterfaceLabels("MsgInvalidNumberofDocInMarkup").elem2 + CStr(ListDoc.ListCount) + vbCrLf + InterfaceLabels("MsgInvalidNumberofDocInCfgRec").elem2 + CStr(FileCounter), True)
                End If
            Else
                ret = True
            End If
        End If
        If ret Then EnableObjects (True)
    End If
    End With
End Sub
