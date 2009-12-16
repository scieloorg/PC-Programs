Attribute VB_Name = "ISIS32"
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'   Copyright (c) 1996 by

'   United Nations Educational Scientific and Cultural Organization.
'                                &
'   Latin American and Caribbean Center on Health Sciences Information /
'   PAHO-WHO.
'   All Rights Reserved.
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


'-------------------- ISIS_DLL application functions --------------------'

Declare Function IsisAppAcTab Lib "isis32.dll" (ByVal AppHandle&, ByVal AcTab$) As Long
Declare Function IsisAppDebug Lib "isis32.dll" (ByVal AppHandle&, ByVal Flag&) As Long
Declare Function IsisAppDelete Lib "isis32.dll" (ByVal AppHandle&) As Long
Declare Function IsisAppLogFile Lib "isis32.dll" (ByVal AppHandle&, ByVal FileName$) As Long
Declare Function IsisAppNew Lib "isis32.dll" () As Long
Declare Function IsisAppParGet Lib "isis32.dll" (ByVal AppHandle&, ByVal ParIn$, ByVal ParOut$, ByVal AreaSize&) As Long
Declare Function IsisAppParSet Lib "isis32.dll" (ByVal AppHandle&, ByVal AppAreap$) As Long
Declare Function IsisAppUcTab Lib "isis32.dll" (ByVal AppHandle&, ByVal UcTab$) As Long


'-------------------- ISIS_DLL dll functions ----------------------------'

Declare Function IsisDllVersion Lib "isis32.dll" () As Single


'-------------------- ISIS_DLL link functions ----------------------------'

Declare Function IsisLnkIfLoad Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisLnkIfLoadEx Lib "isis32.dll" (ByVal handle&, ByVal ResetFlag&, ByVal Posts&, ByVal Balan&) As Long
Declare Function IsisLnkSort Lib "isis32.dll" (ByVal handle&) As Long


'-------------------- ISIS_DLL record functions -------------------------'

Declare Function IsisRecControlMap Lib "isis32.dll" (ByVal handle&, p As IsisRecControl) As Long
Declare Function IsisRecCopy Lib "isis32.dll" (ByVal HandleFrom&, ByVal IndexFrom&, ByVal HandleTo&, ByVal IndexTo&) As Long
Declare Function IsisRecDirMap Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal FirstPos&, ByVal LastPos&, p As IsisRecDir) As Long
Declare Function IsisRecDummy Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecDump Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal FieldArea$, ByVal AreaSize&) As Long
Declare Function IsisRecField Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal tag&, ByVal Occ&, ByVal FieldArea$, ByVal AreaSize&) As Long
Declare Function IsisRecFieldN Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal pos&, ByVal FieldArea$, ByVal AreaSize&) As Long
Declare Function IsisRecFieldOcc Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal tag&) As Long
Declare Function IsisRecFieldUpdate Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal FldUpd$) As Long
Declare Function IsisRecFormat Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Farea$, ByVal AreaSize&) As Long
Declare Function IsisRecFormatCisis Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Farea$, ByVal FareaSize&) As Long
Declare Function IsisRecFormatCisisEx Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal LineSize&, ByVal Farea$, ByVal FareaSize&) As Long
Declare Function IsisRecFormatEx Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal LineSize&, ByVal Farea$, ByVal AreaSize&) As Long
Declare Function IsisRecIfUpdate Lib "isis32.dll" (ByVal handle&, ByVal Mfn&) As Long
Declare Function IsisRecIfUpdateEx Lib "isis32.dll" (ByVal handle&, ByVal BeginMfn&, ByVal EndMfn&, ByVal KeepPending&) As Long
Declare Function IsisRecIsoRead Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecIsoWrite Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecLeaderMap Lib "isis32.dll" (ByVal handle&, ByVal index&, p As IsisRecLeader) As Long
Declare Function IsisRecLnk Lib "isis32.dll" (ByVal handle&, ByVal BeginMfn&, ByVal EndMfn&) As Long
Declare Function IsisRecMerge Lib "isis32.dll" (ByVal HandleFrom&, ByVal IndexFrom&, ByVal HandleTo&, ByVal IndexTo&) As Long
Declare Function IsisRecMfn Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecMfnChange Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Mfn&) As Long
Declare Function IsisRecNew Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecNewLock Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecNvf Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecRead Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Mfn&) As Long
Declare Function IsisRecReadLock Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Mfn&) As Long
Declare Function IsisRecShelfSize Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Memory&) As Long
Declare Function IsisRecSubField Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal tag&, ByVal FldOcc&, ByVal SubField$, ByVal SubFieldArea$, ByVal AreaSize&) As Long
Declare Function IsisRecSubFieldEx Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal tag&, ByVal FldOcc&, ByVal SubField$, ByVal SubFldOcc&, ByVal SubFieldArea$, ByVal AreaSize&) As Long
Declare Function IsisRecUndelete Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecUnlock Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecUnlockForce Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecUpdate Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal FieldArea$) As Long
Declare Function IsisRecWrite Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecWriteLock Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long
Declare Function IsisRecWriteUnlock Lib "isis32.dll" (ByVal handle&, ByVal index&) As Long


'-------------------- ISIS_DLL space functions -------------------------'

Declare Function IsisSpaDb Lib "isis32.dll" (ByVal handle&, ByVal NameDb$) As Long
Declare Function IsisSpaDf Lib "isis32.dll" (ByVal handle&, ByVal NameDf$) As Long
Declare Function IsisSpaDelete Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisSpaFmt Lib "isis32.dll" (ByVal handle&, ByVal NameFmt$) As Long
Declare Function IsisSpaFst Lib "isis32.dll" (ByVal handle&, ByVal NameFst$) As Long
Declare Function IsisSpaGf Lib "isis32.dll" (ByVal handle&, ByVal NameGf$) As Long
Declare Function IsisSpaHeaderMap Lib "isis32.dll" (ByVal handle&, p As IsisSpaHeader) As Long
Declare Function IsisSpaIf Lib "isis32.dll" (ByVal handle&, ByVal NameIf$) As Long
Declare Function IsisSpaIfCreate Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisSpaIsoDelim Lib "isis32.dll" (ByVal handle&, ByVal RecDelim$, ByVal FieldDelim$) As Long
Declare Function IsisSpaIsoIn Lib "isis32.dll" (ByVal handle&, ByVal FileName$) As Long
Declare Function IsisSpaIsoOut Lib "isis32.dll" (ByVal handle&, ByVal FileName$) As Long
Declare Function IsisSpaIsoOutCreate Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisSpaLnkFix Lib "isis32.dll" (ByVal handle&, ByVal IFix&, ByVal OFix&) As Long
Declare Function IsisSpaMf Lib "isis32.dll" (ByVal handle&, ByVal NameMst$) As Long
Declare Function IsisSpaMfCreate Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisSpaMfUnlockForce Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisSpaMultiOn Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisSpaMultiOff Lib "isis32.dll" (ByVal handle&) As Long
Declare Function IsisSpaName Lib "isis32.dll" (ByVal handle&, ByVal NameSpace$) As Long
Declare Function IsisSpaNew Lib "isis32.dll" (ByVal AppHandle&) As Long
Declare Function IsisSpaPft Lib "isis32.dll" (ByVal handle&, ByVal NamePft$) As Long
Declare Function IsisSpaPftCisis Lib "isis32.dll" (ByVal handle&, ByVal NamePft$) As Long
Declare Function IsisSpaRecDelim Lib "isis32.dll" (ByVal handle&, ByVal BeginDelim$, ByVal EndDelim$) As Long
Declare Function IsisSpaRecShelves Lib "isis32.dll" (ByVal handle&, ByVal MaxMst&) As Long
Declare Function IsisSpaStw Lib "isis32.dll" (ByVal handle&, ByVal NameStw$) As Long
Declare Function IsisSpaTrmShelves Lib "isis32.dll" (ByVal handle&, ByVal MaxMst&) As Long

'-------------------- ISIS_DLL search functions -------------------------'

Declare Function IsisSrcHeaderMap Lib "isis32.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal SearchNo&, p As IsisSrcHeader) As Long
Declare Function IsisSrcHitMap Lib "isis32.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal SearchNo&, ByVal FirstPos&, ByVal LastPos&, p As IsisSrcHit) As Long
Declare Function IsisSrcLogFileFlush Lib "isis32.dll" (ByVal AppHandle&, ByVal TSFNum&) As Long
Declare Function IsisSrcLogFileSave Lib "isis32.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal FileName$) As Long
Declare Function IsisSrcLogFileUse Lib "isis32.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal FileName$) As Long
Declare Function IsisSrcMfnMap Lib "isis32.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal SearchNo&, ByVal FirstPos&, ByVal LastPos&, p As IsisSrcMfn) As Long
Declare Function IsisSrcSearch Lib "isis32.dll" (ByVal handle&, ByVal TSFNum&, ByVal Bool$, p As IsisSrcHeader) As Long


'-------------------- ISIS_DLL term functions -------------------------'

Declare Function IsisTrmMfnMap Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal FirstPos&, ByVal LastPos&, p As IsisTrmMfn) As Long
Declare Function IsisTrmPostingMap Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal FirstPos&, ByVal LastPos&, p As IsisTrmPosting) As Long
Declare Function IsisTrmReadMap Lib "isis32.dll" (ByVal handle&, ByVal index&, p As IsisTrmRead) As Long
Declare Function IsisTrmReadNext Lib "isis32.dll" (ByVal handle&, ByVal index&, p As IsisTrmRead) As Long
Declare Function IsisTrmReadPrevious Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Prefix$, p As IsisTrmRead) As Long
Declare Function IsisTrmShelfSize Lib "isis32.dll" (ByVal handle&, ByVal index&, ByVal Memory&) As Long


'-------------------- General functions -------------------------------'

Declare Function OemToCharBuff Lib "user32" Alias "OemToCharBuffA" (ByVal lpszSrc As String, ByVal lpszDst As String, ByVal cchDstLength As Long) As Long
Declare Function CharToOemBuff Lib "user32" Alias "CharToOemBuffA" (ByVal lpszSrc As String, ByVal lpszDst As String, ByVal cchDstLength As Long) As Long
Declare Function SetHandleCount Lib "kernel32" (ByVal wNumber As Long) As Long


















