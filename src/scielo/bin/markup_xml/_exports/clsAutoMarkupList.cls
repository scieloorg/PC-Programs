VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsAutoMarkupList"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

Private automataList As New collection
'-------------------------------------
Private mErr As New clsErrList
Const errIDObj As String = "205"
Public keyIsISSN As Boolean

Public Sub LoadAutomata(conf As clsConfig)
  Dim automata As clsAutoMarkup, token As New clsToken
  Dim line As String, aux As String, f As Integer
  Dim k As String
  Dim automataFile As New clsFile
  
  
  
  Const errIDMet As String = "01"
  '-----------------------------
  On Error GoTo errlog
  
  If automataFile.existFile(conf.directory & conf.fileAutomata) Then
    f = FreeFile
    
    Open conf.directory & conf.fileAutomata For Input As #f
    While Not EOF(f)
      Line Input #f, line
      
      If Len(Trim$(line)) > 0 Then
        With token
          Set automata = New clsAutoMarkup
          .GetTokens line, aux: automata.key = aux
          k = automata.key
          .GetTokens line, aux: automata.initialTag = aux
          .GetTokens line, aux: automata.automataFile = aux
          .GetTokens line, aux: automata.tagsFile = aux
          
        End With
        
        If automataFile.existFile(MyMacro.markupprg_path & "\" & automata.automataFile) Then
          automataList.add automata, automata.key
        End If
        
      End If
      
    Wend
      If (Len(k) = 9) And (Mid(k, 5, 1) = "-") Then
          keyIsISSN = True
      End If
      
    Close #f
  Else
    MsgBox conf.directory & conf.fileAutomata & " " & conf.msgMissingFile
  End If
  '---------------------
  Set automata = Nothing: Set token = Nothing
  Exit Sub
errlog:
  MsgBox "LoadAutomata (Journal List): " & conf.directory & conf.fileAutomata & " line: " & line & vbCrLf & err.description
  
  With mErr
    .LoadErr conf
    .BuildLog errIDObj & errIDMet, conf
  End With
  Set automata = Nothing: Set token = Nothing
End Sub

Public Function ReturnAutomata(key As String) As clsAutoMarkup
  On Error Resume Next
  key = Trim$(key)
  
  
  If val(key) = 0 Or Mid(key, 5, 1) = "-" Then
    Set ReturnAutomata = automataList.item(key)
    If err.number <> 0 Then
      ReturnAutomata = Nothing
    End If
  Else
    Set ReturnAutomata = automataList.item(val(key))
  End If
End Function
