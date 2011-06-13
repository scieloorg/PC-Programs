VERSION 5.00
Begin VB.Form FrmCodes 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Codes"
   ClientHeight    =   6015
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   10770
   Icon            =   "FrmEditCodes.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   6015
   ScaleWidth      =   10770
   ShowInTaskbar   =   0   'False
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdSave 
      Caption         =   "CmdSave"
      Height          =   375
      Left            =   8040
      TabIndex        =   7
      Top             =   5520
      Width           =   1215
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   9360
      TabIndex        =   0
      Top             =   5520
      Width           =   1215
   End
   Begin VB.Frame Frame1 
      Height          =   5295
      Left            =   120
      TabIndex        =   1
      Top             =   120
      Width           =   10575
      Begin VB.TextBox Text2 
         Height          =   375
         Left            =   2760
         TabIndex        =   18
         Top             =   4800
         Width           =   2415
      End
      Begin VB.TextBox Text3 
         Height          =   375
         Left            =   5280
         TabIndex        =   17
         Top             =   4800
         Width           =   2535
      End
      Begin VB.TextBox Text4 
         Height          =   375
         Left            =   7920
         TabIndex        =   16
         Top             =   4800
         Width           =   2535
      End
      Begin VB.CheckBox CheckLangDepending 
         Caption         =   "language depending"
         Height          =   375
         Left            =   5160
         TabIndex        =   15
         Top             =   720
         Width           =   3255
      End
      Begin VB.CommandButton CmdLoadTable 
         Caption         =   "..."
         Height          =   375
         Left            =   4200
         TabIndex        =   14
         Top             =   240
         Width           =   1215
      End
      Begin VB.CheckBox CheckEnableUserEditing 
         Caption         =   "Check1"
         Height          =   375
         Left            =   120
         TabIndex        =   13
         Top             =   720
         Width           =   3255
      End
      Begin VB.CommandButton CmdNewCode 
         Caption         =   "+"
         Height          =   375
         Left            =   3360
         TabIndex        =   12
         Top             =   3960
         Width           =   855
      End
      Begin VB.CommandButton CmdChange 
         Caption         =   "î"
         Height          =   375
         Left            =   5400
         TabIndex        =   11
         Top             =   3960
         Width           =   1215
      End
      Begin VB.CommandButton CmdDelete 
         Caption         =   "-"
         Height          =   375
         Left            =   4320
         TabIndex        =   10
         Top             =   3960
         Width           =   855
      End
      Begin VB.TextBox TextCode 
         Height          =   375
         Left            =   120
         TabIndex        =   8
         Top             =   4800
         Width           =   2415
      End
      Begin VB.ListBox List1 
         Height          =   2595
         Left            =   120
         TabIndex        =   3
         Top             =   1200
         Width           =   10215
      End
      Begin VB.ComboBox ComboTableName 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   2
         Top             =   240
         Width           =   3855
      End
      Begin VB.Label LabCode 
         Caption         =   "Code"
         Height          =   255
         Left            =   120
         TabIndex        =   9
         Top             =   4560
         Width           =   2175
      End
      Begin VB.Label LabIdioma 
         Caption         =   "Label3"
         Height          =   255
         Index           =   2
         Left            =   7920
         TabIndex        =   6
         Top             =   4560
         Width           =   2415
      End
      Begin VB.Label LabIdioma 
         Caption         =   "Label2"
         Height          =   255
         Index           =   1
         Left            =   5280
         TabIndex        =   5
         Top             =   4560
         Width           =   2415
      End
      Begin VB.Label LabIdioma 
         Caption         =   "Label1"
         Height          =   255
         Index           =   0
         Left            =   2760
         TabIndex        =   4
         Top             =   4560
         Width           =   2415
      End
   End
End
Attribute VB_Name = "FrmCodes"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

'Private MyCodes As ClCodes
Private CodeDAO As clsCodeDAO
Private current As String
Private USED_BY_ADM As Boolean
Private listItems() As String

Public Sub loadForm(pathdb As String, filedb As String, label As String)
    Dim r As ClsTextCollection
    Dim i As Long
    
    If filedb = DBNEWCODEFILE Then
        USED_BY_ADM = False
    Else
        USED_BY_ADM = True
    End If
    
    FrmCodes.Caption = label
    loadInterfaceLabels
    
    Set CodeDAO = New clsCodeDAO
    Call CodeDAO.setDB(pathdb, filedb, label)
    
    
    If USED_BY_ADM Then
        Set r = CodeDAO.getTablesName(Not USED_BY_ADM)
    Else
        Dim dao As clsCodeDAO
        Set dao = New clsCodeDAO
        Call dao.setDB(pathdb, DBCODEFILE, label)
    
        Set r = dao.getTablesName(Not USED_BY_ADM)
    End If
    For i = 1 To r.Count
        ComboTableName.AddItem r.Item(i).text
    Next
    
    Call displayTextBoxes(False)
    FrmCodes.Show vbModal
End Sub

Private Sub CheckLangDepending_Click()
    Call displayTextBoxes(CheckLangDepending.value)
End Sub

Private Sub CmdChange_Click()
    
'ComboTableName.Enabled = False

    If CheckTexts Then
    Call displayEditingCommands(False)
    listItems(List1.ListIndex) = Mid(List1.List(List1.ListIndex), 1, InStr(List1.List(List1.ListIndex), "|")) + " " + Text2.text + " | " + Text3.text + " | " + Text4.text
    List1.List(List1.ListIndex) = Mid(List1.List(List1.ListIndex), 1, InStr(List1.List(List1.ListIndex), "|")) + " " + Text2.text + " | " + Text3.text + " | " + Text4.text
    Text2.text = ""
    Text3.text = ""
    Text4.text = ""
    TextCode.text = ""
    End If
End Sub

Function CheckTexts() As Boolean
    Dim text As String
    If FrmCodes.CheckLangDepending.value = 1 Then
        If Trim(Text2.text) <> "" Then
            text = Text2.text
        Else
            If Trim(Text3.text) <> "" Then
                text = Text3.text
            Else
                If Trim(Text4.text) <> "" Then
                    text = Text4.text
                Else
                    text = ""
                End If
            End If
        End If
        If Trim(text) <> "" Then
            If Trim(Text2.text) = "" Then
                Text2.text = text
            End If
            If Trim(Text3.text) = "" Then
                Text3.text = text
            End If
            If Trim(Text4.text) = "" Then
                Text4.text = text
            End If
            
        End If
    Else
        If Trim(Text2.text) <> "" Then
            text = Text2.text
        End If
        
        If Trim(text) <> "" Then
            If Trim(Text2.text) = "" Then
                Text2.text = text
            End If
        End If
        Text3.text = ""
        Text4.text = ""
        
    End If
    CheckTexts = (Len(Trim(text)) > 0)
End Function
Private Sub CmdClose_Click()
    If isChanged Then
        CloseQuestion
    Else
        Unload Me
    End If
End Sub
Private Sub CloseQuestion()
    Dim res As VbMsgBoxResult
    
    res = MsgBox(ConfigLabels.getLabel("msgAsksave"), vbYesNoCancel)
    Select Case res
    Case vbYes
        save
        Unload Me
    Case vbNo
        Unload Me
    Case vbCancel
        
    End Select

End Sub


Private Function retCodeRecord() As clsTable
    Dim i As Long
    Dim k As Long
    Dim table As New clsTable
    Dim c As clsCode
    Dim Item() As String
    Dim tr As clsText
    
    table.label = ComboTableName.text
    If CheckEnableUserEditing.value Then
        table.status = "1"
    End If
    
    Set table.code_translations = New clsCodeCollection
    For k = 1 To List1.ListCount
        Item = Split(listItems(k - 1), " | ")
        
        Set c = table.code_translations.Item(Item(0))
        If c Is Nothing Then
            Set c = New clsCode
            c.code = Item(0)
            
            Call table.code_translations.Add(c, c.code)
            Set c.translations = New ClsTextCollection
        End If
        If CheckLangDepending.value Then
            For i = 1 To IdiomsInfo.Count
                Set tr = New clsText
                tr.text = Item(i)
                tr.lang = IdiomsInfo(i).code
                Call c.translations.Add(tr, IdiomsInfo(i).code)
            Next
        Else
            Set tr = New clsText
            tr.text = Item(1)
            tr.lang = "nolang"
            Call c.translations.Add(tr, tr.lang)
        End If
    Next
    Set retCodeRecord = table
End Function
Private Function loadCodeRecord(label As String, Optional theList As ListBox) As Boolean
    Dim r As clsTable
    Dim i As Long
    Dim k As Long
    Dim tr As clsText
    Dim listItem As String
    Dim Item As clsCode
    Dim text As String
    
    current = ""
    
    If theList Is Nothing Then
        Set theList = List1
    End If
    
    Set r = CodeDAO.getCodes(label)
    If r Is Nothing Then
    Else
    
        If r.status = "1" Then
            CheckEnableUserEditing.value = 1
        Else
            CheckEnableUserEditing.value = 0
        End If
        
        If r.code_translations Is Nothing Then
            CheckLangDepending.value = 0
        Else
            If (r.code_translations.Item(1).translations.Count > 1) Then
                CheckLangDepending.value = 1
            Else
                CheckLangDepending.value = 0
            End If
        End If
        
        theList.Clear
        CmdDelete.Enabled = False
        CmdChange.Enabled = False
        
        If Not r.code_translations Is Nothing Then
            For i = 1 To r.code_translations.Count
                Set Item = r.code_translations.Item(i)
                listItem = Item.code
                If CheckLangDepending.value = 1 Then
                    For k = 1 To IdiomsInfo.Count
                        Set tr = Item.translations(IdiomsInfo(k).code)
                        If tr Is Nothing Then
                            text = ""
                        Else
                            
                            text = tr.text
                        End If
                        listItem = listItem + " | " + text
                    Next
                Else
                    listItem = listItem + " | " + Item.translations(1).text + " |  | "
                End If
                theList.AddItem (listItem)
                ReDim Preserve listItems(theList.ListCount)
                listItems(theList.ListCount - 1) = listItem
                current = current + listItem
            Next
            Call displayTextBoxes((CheckLangDepending.value = 1))
        End If
    End If
End Function
Private Function old2_loadCodeRecord(label As String, Optional theList As ListBox) As Boolean
    Dim r As clsTable
    Dim i As Long
    Dim k As Long
    Dim tr As clsText
    Dim listItem As String
    Dim Item As clsCode
    Dim text As String
    
    current = ""
    
    If theList Is Nothing Then
        Set theList = List1
    End If
    
    Set r = CodeDAO.getCodes(label)
    If r Is Nothing Then
    Else
    
        If r.status = "1" Then
            CheckEnableUserEditing.value = 1
        Else
            CheckEnableUserEditing.value = 0
        End If
        
        If r.code_translations Is Nothing Then
            CheckLangDepending.value = 0
        Else
            If (r.code_translations.Item(1).translations.Count > 1) Then
                CheckLangDepending.value = 1
            Else
                CheckLangDepending.value = 0
            End If
        End If
        
        theList.Clear
        CmdDelete.Enabled = False
        CmdChange.Enabled = False
        
        If Not r.code_translations Is Nothing Then
            If CheckLangDepending.value = 1 Then
                
                For i = 1 To r.code_translations.Count
                    Set Item = r.code_translations.Item(i)
                    
                    
                    listItem = Item.code
                    For k = 1 To IdiomsInfo.Count
                        Set tr = Item.translations(IdiomsInfo(k).code)
                        If tr Is Nothing Then
                            text = ""
                        Else
                            
                            text = tr.text
                        End If
                        listItem = listItem + " | " + text
                    Next
                    theList.AddItem (listItem)
                    ReDim Preserve listItems(theList.ListCount)
                    listItems(theList.ListCount - 1) = listItem
                    current = current + listItem
                Next
            Else
                listItem = r.code_translations.Item(1).code + " | " + r.code_translations.Item(1).translations(1).text + " |  | "
            End If
            Call displayTextBoxes(r.code_translations.Item(1).translations.Count > 1)
        End If
    End If
End Function

Private Function old_loadCodeRecord(label As String, Optional theList As ListBox) As Boolean
    Dim r As clsTable
    Dim i As Long
    Dim k As Long
    Dim tr As clsText
    Dim Item As String
    
    current = ""
    
    If theList Is Nothing Then
        Set theList = List1
    End If
    
    Set r = CodeDAO.getCodes(label)
    If r Is Nothing Then
    Else
    
        If r.status = "1" Then
            CheckEnableUserEditing.value = 1
        Else
            CheckEnableUserEditing.value = 0
        End If
        
        If r.code_translations Is Nothing Then
                CheckLangDepending.value = 0
        
        Else
            
            If (r.code_translations.Item(1).translations.Count > 1) Then
                CheckLangDepending.value = 1
            Else
                CheckLangDepending.value = 0
            End If
        End If
        
        theList.Clear
        CmdDelete.Enabled = False
        CmdChange.Enabled = False
        
        If Not r.code_translations Is Nothing Then
            For i = 1 To r.code_translations.Count
                Item = r.code_translations.Item(i).code
                If r.code_translations.Item(i).translations.Count = 1 Then
                    Item = Item + " | " + r.code_translations.Item(i).translations(1).text + " |  | "
                Else
                    For k = 1 To IdiomsInfo.Count
                        Set tr = r.code_translations.Item(i).translations(IdiomsInfo(k).code)
                        If tr Is Nothing Then
                        Else
                            Item = Item + " | " + tr.text
                        End If
                    Next
                End If
                theList.AddItem (Item)
                ReDim Preserve listItems(theList.ListCount)
                listItems(theList.ListCount - 1) = Item
                current = current + Item
            Next
            Call displayTextBoxes(r.code_translations.Item(1).translations.Count > 1)
        End If
    End If
End Function
Private Function isChanged() As Boolean
    Dim x As String
    Dim i As Long
     
    For i = 0 To List1.ListCount - 1
        x = x + listItems(i)
    Next
    isChanged = (x <> current)
End Function


Private Sub CmdDelete_Click()
    Dim index As Long
    index = List1.ListIndex
    List1.RemoveItem (index)
    Dim i As Long
    For i = index To List1.ListCount - 1
        listItems(i) = listItems(i + 1)
    Next
    ReDim Preserve listItems(List1.ListCount)
    Call displayEditingCommands(False)
End Sub

Private Sub CmdLoadTable_Click()
    loadCodeRecord (Trim(ComboTableName.text))
End Sub

Private Sub CmdNewCode_Click()
    Dim k As Long
    Dim found As Boolean
    
        If Len(Trim(TextCode.text)) > 0 Then
            While (k < List1.ListCount) And Not found
                If InStr(List1.List(k), TextCode.text + " | ") = 1 Then
                    found = True
                End If
                k = k + 1
            Wend
            If found Then
                MsgBox "FIXME Código já está em uso"
            Else
                If CheckTexts Then
                    
                    ReDim Preserve listItems(List1.ListCount)
                    listItems(List1.ListCount) = TextCode.text + " | " + Text2.text + " | " + Text3.text + " | " + Text4.text
                    List1.AddItem (TextCode.text + " | " + Text2.text + " | " + Text3.text + " | " + Text4.text)
                    TextCode.text = ""
                    Text2.text = ""
                    Text3.text = ""
                    Text4.text = ""
                End If
            End If
        End If
    
End Sub

Private Sub CmdNewTableName_Click()

End Sub

Private Sub CmdSave_Click()
    save
End Sub
Private Sub save()
    Dim r As clsTable
    Dim i As Long
    
    current = ""
    
    For i = 0 To List1.ListCount - 1
        current = current + listItems(i)
    Next
    
    Set r = retCodeRecord()
    
    Call CodeDAO.save(r)
    
    ComboTableName.Enabled = True
End Sub

Private Sub loadInterfaceLabels()
    Dim i As Long
    
    With ConfigLabels
   
    CmdClose.Caption = .getLabel("buttonClose")
    CmdSave.Caption = .getLabel("buttonSave")
    CmdNewCode.Caption = .getLabel("buttonAdd")
    CmdDelete.Caption = .getLabel("buttonRemove")
    CmdChange.Caption = .getLabel("buttonUpdate")
    
    CheckEnableUserEditing.Caption = .getLabel("labCustomizableTable") ' FIXME
    LabCode.Caption = .getLabel("labCode")
    
    'CmdNewCode.Visible = USED_BY_ADM
    'CmdDelete.Visible = USED_BY_ADM
    
    CmdChange.Enabled = False
    CmdDelete.Enabled = False
    CmdNewCode.Enabled = True
    
    CheckEnableUserEditing.Visible = USED_BY_ADM
    CheckLangDepending.Visible = USED_BY_ADM
    
    End With
    
    For i = 1 To IdiomsInfo.Count
        LabIdioma(i - 1).Caption = IdiomsInfo(i).label
    Next
    
    
End Sub



Private Sub ComboTableName_Change()
    List1.Clear
    Call displayEditingCommands(False)
    If USED_BY_ADM Then
    Else
        
    ComboTableName.ListIndex = 0
    End If
End Sub

Private Sub List1_Click()
    Dim t() As String
    t = Split(listItems(List1.ListIndex), " | ")
    TextCode.text = t(0)
    
    Call displayEditingCommands(True)
    
    Text2.text = t(1)
    If UBound(t) > 1 Then
    Text3.text = t(2)
    Text4.text = t(3)
    End If
End Sub

Private Sub displayTextBoxes(isLangDep As Boolean)
        Dim i As Long
        LabIdioma(0).Visible = (isLangDep)
        For i = 1 To 2
            LabIdioma(i).Visible = (isLangDep)
            
        Next
        Text4.Visible = isLangDep
        Text3.Visible = isLangDep
        
        
End Sub
Private Sub displayEditingCommands(status As Boolean)
    CmdNewCode.Enabled = Not status
    CmdDelete.Enabled = status
    CmdChange.Enabled = status
    TextCode.Enabled = Not status
    'Text2.Enabled = status
    'Text3.Enabled = status
    'Text4.Enabled = status
End Sub

