VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "clsConfig"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Public directory As String
'-------------------------
Public prg_name As String
Public parser As String
Private language As String
Private firstHour
Private lastHour
Private markupResponsible As String
'----------------------------------
Public fileAttrib As String
Public fileBar As String
Public fileIssue As String
Public fileTemp As String
Public fileLink As String
Public fileErr As String
Public fileAutomata As String
Public fileTagsAutomata As String
'-------------------------
Public msgInvalid As String
Public msgType     As String
Public msgSelection As String
Public msgInserting As String
Public msgDeleting As String
Public msgOpenFile As String
Public msgSure As String
Public msgMoreLater As String
Public msgAutomatic As String
Public msgAutomaticErr As String
Public msgDefaultDirectories As String
'----------------------------
Public titleAttribute As String
Public titleTag As String
Public titleDelete As String
Public titleOpenFile As String
Public titleFinish As String
Public titleStart As String
Public titleConfig As String
Public titleErr As String
'--------------------------
Public tooltipsDown As String
Public tooltipsUp As String
'----------------------------
Public MainModule As String
'--------------------------
Public BarMarkup As String
'-------------------------
Public STAGO As String
Public ETAGO As String
Public TAGC As String
Public slash As String
Public entitySTAGO As String
Public entityTAGC As String
'---------------------
Public logExtent As String
Public txtExtent As String
'-------------------------
Public TagSize As Integer
'------------------------
Public tagConf0 As String
Public tagConf1 As String
'------------------------
Public textOK As String
Public textCANCEL As String
Public textClear As String
Public textWrite As String
Public titlefrmArticle As String
Public titleFields As String
Public titlefrmAttribute As String
Public titlefrmConfig As String
Public titleLanguage As String
Public titleResponsible As String
Public optionEnglish As String
Public optionSpanish As String
Public optionPortuguese As String
'----------------------------
Public buttonStop As String
Public buttonChange As String
Public buttonDelete As String
Public buttonAutomatic As String
Public buttonHelp As String
'--------------------------

Public Function GetResponsible() As String
  GetResponsible = markupResponsible
End Function

Public Sub SetResponsible(mr As String)
  markupResponsible = mr
End Sub

Public Function GetLanguage() As String
  GetLanguage = language
End Function

Public Sub SetLanguage(l As String)
  language = l
End Sub

Public Sub SetFirstHour()
  firstHour = Time
End Sub

Public Function GetFirstHour() As Variant
  GetFirstHour = firstHour
End Function

Public Sub SetLastHour()
  lastHour = Time
End Sub

Public Function GetLastHour() As Variant
  GetLastHour = lastHour
End Function

Public Function GetMarkupTime() As String
  Dim fH, fM, fS, lH, lM, lS
  Dim TL As Long, TF As Long, t As Long
  Dim h As Integer, m As Integer, s As Integer
  '-------------------------------------------
  lH = Hour(lastHour):  lM = Minute(lastHour):  lS = Second(lastHour)
  fH = Hour(firstHour): fM = Minute(firstHour): fS = Second(firstHour)
  
  lM = lM * 60: lH = lH * 3600: TL = lH + lM + lS
  fM = fM * 60: fH = fH * 3600: TF = fH + fM + fS
  
  t = TL - TF
  
  h = t \ 3600: m = (t Mod 3600) \ 60: s = (t Mod 3600) Mod 60
  
  GetMarkupTime = Str(h) & "h " & Str(m) & "min " & Str(s) & "s"
  
End Function

Public Sub LoadPublicValues()
  'Const projDir = "C:\Scielo\Bin\Markup\"
  Const enFile = "en_conf.mds"
  Const spFile = "es_conf.mds"
  Const ptFile = "pt_conf.mds"
  Const defaultFile = "default.mds"
  '--------------------------------
  Dim aux As String, ok As Boolean
    
  projDir = App.path & "\"
  Open projDir & defaultFile For Input As #2
  Input #2, aux, language
  Input #2, aux, markupResponsible
  Close #2
  '-------
  Select Case language
    Case "en"
      Open projDir & "\" & enFile For Input As #2:      ok = True
    Case "pt"
      Open projDir & "\" & ptFile For Input As #2:      ok = True
    Case "sp"
      Open projDir & "\" & spFile For Input As #2:      ok = True
  End Select
  If ok = True Then
    Input #2, aux, directory: Input #2, aux, prg_name
    Input #2, aux, parser
    Input #2, aux, fileAttrib: Input #2, aux, fileBar
    Input #2, aux, fileIssue:  Input #2, aux, fileTemp
    Input #2, aux, fileLink: Input #2, aux, fileErr
    Input #2, aux, fileAutomata: Input #2, aux, fileTagsAutomata
    Input #2, aux, msgInvalid:  Input #2, aux, msgType
    Input #2, aux, msgSelection:  Input #2, aux, msgInserting
    Input #2, aux, msgDeleting:  Input #2, aux, msgOpenFile
    Input #2, aux, msgSure:  Input #2, aux, msgMoreLater
    Input #2, aux, msgAutomatic: Input #2, aux, msgAutomaticErr
    Input #2, aux, msgDefaultDirectories
    Input #2, aux, titleAttribute: Input #2, aux, titleTag
    Input #2, aux, titleDelete: Input #2, aux, titleOpenFile
    Input #2, aux, titleFinish: Input #2, aux, titleStart
    Input #2, aux, titleConfig: Input #2, aux, titleErr
    Input #2, aux, tooltipsDown: Input #2, aux, tooltipsUp
    Input #2, aux, MainModule
    Input #2, aux, BarMarkup: Input #2, aux, STAGO
    Input #2, aux, ETAGO: Input #2, aux, TAGC
    Input #2, aux, slash
    Input #2, aux, entitySTAGO: Input #2, aux, entityTAGC
    Input #2, aux, logExtent
    Input #2, aux, txtExtent: Input #2, aux, TagSize
    Input #2, aux, tagConf0: Input #2, aux, tagConf1
    Input #2, aux, textOK: Input #2, aux, textCANCEL
    Input #2, aux, textClear: Input #2, aux, textWrite
    Input #2, aux, titlefrmArticle: Input #2, aux, titleFields
    Input #2, aux, titlefrmAttribute: Input #2, aux, titlefrmConfig
    Input #2, aux, titleLanguage: Input #2, aux, titleResponsible
    Input #2, aux, optionEnglish: Input #2, aux, optionSpanish
    Input #2, aux, optionPortuguese
    Input #2, aux, buttonStop: Input #2, aux, buttonChange
    Input #2, aux, buttonDelete: Input #2, aux, buttonAutomatic
    Input #2, aux, buttonHelp
    Close #2
  End If

    'leitura do arquivo de configuração comum a todos os programas
  Dim x As ColFileInfo
  Set x = ReadPathsConfigurationFile("..\scielo_paths.ini")
  directory = x("Markup prg").path & "\"
  prg_name = x("Markup prg").filename
  parser = x("SGML Parser Program").path + "\" + x("SGML Parser Program").filename
End Sub
Function ReadPathsConfigurationFile(File As String) As ColFileInfo
    Dim fn As Long
    Dim lineread As String
    Dim Item As ClFileInfo
    Dim key As String
    Dim path As String
    Dim CollectionPaths As ColFileInfo
    Dim req As Long
    
    fn = FreeFile
    Open File For Input As fn
        
    Set CollectionPaths = New ColFileInfo
    
    While Not EOF(fn)
        Line Input #fn, lineread
        If InStr(lineread, "=") > 0 Then
            If InStr(lineread, "Markup prg") > 0 Or InStr(lineread, "SGML Parser Program") > 0 Then
            key = Mid(lineread, 1, InStr(lineread, "=") - 1)
            path = Mid(lineread, InStr(lineread, "=") + 1)
            req = InStr(path, ",required")
            If req > 0 Then
                path = Mid(path, 1, req - 1)
                
            End If
            Set Item = CollectionPaths.Add(key)
            Item.key = key
            If InStr(path, "\") > 0 Then
                Item.path = Mid(path, 1, InStrRev(path, "\") - 1)
                Item.filename = Mid(path, InStrRev(path, "\") + 1)
            Else
                Item.path = ""
                Item.filename = path
            End If
            Item.required = (req > 0)
            End If
        End If
    Wend
    Close fn
    Set ReadPathsConfigurationFile = CollectionPaths
End Function

