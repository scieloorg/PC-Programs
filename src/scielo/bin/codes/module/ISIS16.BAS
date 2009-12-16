Attribute VB_Name = "ISIS16"
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'   Copyright (c) 1996 by

'   United Nations Educational Scientific and Cultural Organization.
'                                &
'   Latin American and Caribbean Center on Health Sciences Information /
'   PAHO-WHO.

'   All Rights Reserved.
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


'-------------------- ISIS_DLL application functions --------------------'

Declare Function IsisAppAcTab Lib "isis16.dll" (ByVal AppHandle&, ByVal AcTab$) As Long
Declare Function IsisAppDebug Lib "isis16.dll" (ByVal AppHandle&, ByVal flag&) As Long
Declare Function IsisAppDelete Lib "isis16.dll" (ByVal AppHandle&) As Long
Declare Function IsisAppLogFile Lib "isis16.dll" (ByVal AppHandle&, ByVal FileName$) As Long
Declare Function IsisAppNew Lib "isis16.dll" () As Long
Declare Function IsisAppParGet Lib "isis16.dll" (ByVal AppHandle&, ByVal ParIn$, ByVal ParOut$) As Long
Declare Function IsisAppParSet Lib "isis16.dll" (ByVal AppHandle&, ByVal AppAreap$) As Long
Declare Function IsisAppUcTab Lib "isis16.dll" (ByVal AppHandle&, ByVal UcTab$) As Long


'-------------------- ISIS_DLL dll functions ----------------------------'

Declare Function IsisDllVersion Lib "isis16.dll" () As Single


'-------------------- ISIS_DLL link functions ----------------------------'

Declare Function IsisLnkIfLoad Lib "isis16.dll" (ByVal Handle&) As Long
Declare Function IsisLnkIfLoadEx Lib "isis16.dll" (ByVal Handle&, ByVal ResetFlag&, ByVal Posts&, ByVal Balan&) As Long
Declare Function IsisLnkSort Lib "isis16.dll" (ByVal Handle&) As Long

'-------------------- ISIS_DLL record functions -------------------------'

Declare Function IsisRecControlMap Lib "isis16.dll" (ByVal Handle&, p As IsisRecControl) As Long
Declare Function IsisRecCopy Lib "isis16.dll" (ByVal HandleFrom&, ByVal IndexFrom&, ByVal HandleTo&, ByVal IndexTo&) As Long
Declare Function IsisRecDirMap Lib "isis16.dll" (ByVal Handle&, ByVal Index&, p As IsisRecDir) As Long
Declare Function IsisRecDummy Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecDump Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal FieldArea$) As Long
Declare Function IsisRecField Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal tag&, ByVal occ&, ByVal FieldArea$) As Long
Declare Function IsisRecFieldN Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal pos&, ByVal FieldArea$) As Long
Declare Function IsisRecFieldOcc Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal tag&) As Long
Declare Function IsisRecFieldUpdate Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal FldUpd$) As Long
Declare Function IsisRecFormat Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Farea$) As Long
Declare Function IsisRecFormatCisis Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Farea$, ByVal FareaSize&) As Long
Declare Function IsisRecFormatCisisEx Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal LineSize&, ByVal Farea$, ByVal FareaSize&) As Long
Declare Function IsisRecFormatEx Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal LineSize&, ByVal Farea$) As Long
Declare Function IsisRecIfUpdate Lib "isis16.dll" (ByVal Handle&, ByVal Mfn&) As Long
Declare Function IsisRecIfUpdateEx Lib "isis16.dll" (ByVal Handle&, ByVal BeginMfn&, ByVal EndMfn&, ByVal KeepPending&) As Long
Declare Function IsisRecIsoRead Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecIsoWrite Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecLeaderMap Lib "isis16.dll" (ByVal Handle&, ByVal Index&, p As IsisRecLeader) As Long
Declare Function IsisRecLnk Lib "isis16.dll" (ByVal Handle&, ByVal BeginMfn&, ByVal EndMfn&) As Long
Declare Function IsisRecMerge Lib "isis16.dll" (ByVal HandleFrom&, ByVal IndexFrom&, ByVal HandleTo&, ByVal IndexTo&) As Long
Declare Function IsisRecMfn Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecMfnChange Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Mfn&) As Long
Declare Function IsisRecNew Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecNewLock Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecNvf Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecRead Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Mfn&) As Long
Declare Function IsisRecReadLock Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Mfn&) As Long
Declare Function IsisRecShelfSize Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Memory&) As Long
Declare Function IsisRecSubField Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal tag&, ByVal FldOcc&, ByVal SubField$, ByVal SubFieldArea$) As Long
Declare Function IsisRecSubFieldEx Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal tag&, ByVal FldOcc&, ByVal SubField$, ByVal SubFldOcc&, ByVal SubFieldArea$) As Long
Declare Function IsisRecUndelete Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecUnlock Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecUnlockForce Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecUpdate Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal FieldArea$) As Long
Declare Function IsisRecWrite Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecWriteLock Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long
Declare Function IsisRecWriteUnlock Lib "isis16.dll" (ByVal Handle&, ByVal Index&) As Long


'-------------------- ISIS_DLL space functions -------------------------'

Declare Function IsisSpaDb Lib "isis16.dll" (ByVal Handle&, ByVal NameDb$) As Long
Declare Function IsisSpaDf Lib "isis16.dll" (ByVal Handle&, ByVal NameDf$) As Long
Declare Function IsisSpaDelete Lib "isis16.dll" (ByVal Handle&) As Long
Declare Function IsisSpaFmt Lib "isis16.dll" (ByVal Handle&, ByVal NameFmt$) As Long
Declare Function IsisSpaFst Lib "isis16.dll" Alias "IsisSpaFST" (ByVal Handle&, ByVal NameFst$) As Long
Declare Function IsisSpaGf Lib "isis16.dll" (ByVal Handle&, ByVal NameGf$) As Long
Declare Function IsisSpaHeaderMap Lib "isis16.dll" (ByVal Handle&, p As IsisSpaHeader) As Long
Declare Function IsisSpaIf Lib "isis16.dll" (ByVal Handle&, ByVal NameIf$) As Long
Declare Function IsisSpaIfCreate Lib "isis16.dll" (ByVal Handle&) As Long
Declare Function IsisSpaIsoDelim Lib "isis16.dll" (ByVal Handle&, ByVal RecDelim$, ByVal FieldDelim$) As Long
Declare Function IsisSpaIsoIn Lib "isis16.dll" (ByVal Handle&, ByVal FileName$) As Long
Declare Function IsisSpaIsoOut Lib "isis16.dll" (ByVal Handle&, ByVal FileName$) As Long
Declare Function IsisSpaIsoOutCreate Lib "isis16.dll" (ByVal Handle&) As Long
Declare Function IsisSpaLnkFix Lib "isis16.dll" (ByVal Handle&, ByVal IFix&, ByVal OFix&) As Long
Declare Function IsisSpaMf Lib "isis16.dll" (ByVal Handle&, ByVal NameMst$) As Long
Declare Function IsisSpaMfCreate Lib "isis16.dll" (ByVal Handle&) As Long
Declare Function IsisSpaMultiOff Lib "isis16.dll" (ByVal Handle&) As Long
Declare Function IsisSpaMultiOn Lib "isis16.dll" (ByVal Handle&) As Long
Declare Function IsisSpaName Lib "isis16.dll" (ByVal Handle&, ByVal NameSpace$) As Long
Declare Function IsisSpaNew Lib "isis16.dll" (ByVal AppHandle&) As Long
Declare Function IsisSpaPft Lib "isis16.dll" (ByVal Handle&, ByVal NamePft$) As Long
Declare Function IsisSpaPftCisis Lib "isis16.dll" (ByVal Handle&, ByVal NamePft$) As Long
Declare Function IsisSpaRecDelim Lib "isis16.dll" (ByVal Handle&, ByVal BeginDelim$, ByVal EndDelim$) As Long
Declare Function IsisSpaRecShelves Lib "isis16.dll" (ByVal Handle&, ByVal MaxMst&) As Long
Declare Function IsisSpaStw Lib "isis16.dll" (ByVal Handle&, ByVal NameStw$) As Long
Declare Function IsisSpaTrmShelves Lib "isis16.dll" (ByVal Handle&, ByVal MaxMst&) As Long

'-------------------- ISIS_DLL search functions -------------------------'

Declare Function IsisSrcHeaderMap Lib "isis16.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal SearchNo&, p As IsisSrcHeader) As Long
Declare Function IsisSrcHitMap Lib "isis16.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal SearchNo&, ByVal HitNumber&, p As IsisSrcHit) As Long
Declare Function IsisSrcLogFileFlush Lib "isis16.dll" (ByVal AppHandle&, ByVal TSFNum&) As Long
Declare Function IsisSrcLogFileSave Lib "isis16.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal FileName$) As Long
Declare Function IsisSrcLogFileUse Lib "isis16.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal FileName$) As Long
Declare Function IsisSrcMfnMap Lib "isis16.dll" (ByVal AppHandle&, ByVal TSFNum&, ByVal SearchNo&, ByVal FirstPos&, ByVal LastPos&, p As IsisSrcMfn) As Long
Declare Function IsisSrcSearch Lib "isis16.dll" (ByVal Handle&, ByVal TSFNum&, ByVal Bool$, p As IsisSrcHeader) As Long


'-------------------- ISIS_DLL term functions -------------------------'

Declare Function IsisTrmMfnMap Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal FirstPos&, ByVal LastPos&, p As IsisTrmMfn) As Long
Declare Function IsisTrmPostingMap Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal PostingNumber&, p As IsisTrmPosting) As Long
Declare Function IsisTrmRead Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Key$) As Long
Declare Function IsisTrmReadNext Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Key$) As Long
Declare Function IsisTrmReadPrevious Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Prefix, ByVal Key$) As Long
Declare Function IsisTrmShelfSize Lib "isis16.dll" (ByVal Handle&, ByVal Index&, ByVal Memory&) As Long


'-------------------- General functions -------------------------------'

Declare Function OemToAnsi Lib "Keyboard" (ByVal lpOemStr As String, ByVal lpAnsiStr As String) As Long
Declare Sub OemToAnsiBuff Lib "Keyboard" (ByVal lpOemStr As String, ByVal lpAnsiStr As String, ByVal nLength As Long)
Declare Function AnsiToOem Lib "Keyboard" (ByVal lpAnsiStr As String, ByVal lpOemStr As String) As Long
Declare Sub AnsiToOemBuff Lib "Keyboard" (ByVal lpAnsiStr As String, ByVal lpOemStr As String, ByVal nLength As Long)
Declare Function SetHandleCount Lib "Kernel" (ByVal wNumber As Long) As Long















