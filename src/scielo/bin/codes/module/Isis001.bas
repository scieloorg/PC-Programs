Attribute VB_Name = "ISIS001"
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'   Copyright (c) 1996 by

'   United Nations Educational Scientific and Cultural Organization.
'                                &
'   Latin American and Caribbean Center on Health Sciences Information /
'   PAHO-WHO.

'   All Rights Reserved.
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

'                            ISIS_DLL Global Constants

'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_


' ----------- Debug Flags ----------------------

Global Const SHOW_NEVER = 0
Global Const SHOW_FATAL = 1
Global Const SHOW_ALWAYS = 3

Global Const EXIT_NEVER = 0
Global Const EXIT_FATAL = 16
Global Const EXIT_ALWAYS = 48

Global Const DEBUG_VERY_LIGHT = SHOW_NEVER Or EXIT_NEVER
Global Const DEBUG_LIGHT = SHOW_FATAL Or EXIT_FATAL
Global Const DEBUG_HARD = SHOW_ALWAYS Or EXIT_FATAL
Global Const DEBUG_VERY_HARD = SHOW_ALWAYS Or EXIT_ALWAYS

' ----------------------------------------------


Global Const KEY_LENGTH = 30
Global Const IFBSIZE = 512

Global Const SRC_EXPR_LENGTH = 512
Global Const MAXPATHLEN = 63

Global Const KEY_LENGTH1 = KEY_LENGTH + 1
Global Const SRC_EXPR_LENGTH1 = SRC_EXPR_LENGTH + 1
Global Const MAXPATHLEN1 = MAXPATHLEN + 1

Global Const MAXMFRL = 8192          'max record length.



'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

'                            ISIS_DLL Structures

'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

' NOTE: The structures DOES NOT necessarily reflects the actual
'       disk file layout.


Type IsisRecControl

    ctlmfn          As Long                     'gdb ctlmfn.
    nxtmfn          As Long                     'gdb nxtmfn.
    nxtmfb          As Long                     'gdb nxtmfb.
    nxtmfp          As Long                     'gdb nxtmfp - offset.
    mftype          As Long                     'gdb mftype.
    reccnt          As Long                     'gdb reccnt.
    mfcxx1          As Long                     'gdb mfcxx1.
    mfcxx2          As Long                     'gdb mfcxx2 - MULTI: Data entry lock.
    mfcxx3          As Long                     'gdb mfcxx3 - MULTI: Exclusive write lock.

End Type


Type IsisRecDir

    tag             As Long                     'field tag entry.
    pos             As Long                     'field position.
    len             As Long                     'field length entry.

End Type


Type IsisRecLeader

    Mfn             As Long                     'gdb mfn.
    mfrl            As Long                     'gdb mfrl - MULTI: record being updated.
    mfbwb           As Long                     'gdb mfbwb.
    mfbwp           As Long                     'gdb mfbwp - offset.
    base            As Long                     'gdb base (MSNVSPLT).
    nvf             As Long                     'gdb nvf.
    Issue_status          As Long                     'gdb Issue_status.

End Type


Type IsisSpaHeader

    handle          As Long                     'pointer to ISIS_SPACE.
    name            As String * MAXPATHLEN1     'ISIS_SPACE name.
    cipar           As String * MAXPATHLEN1     'cipar file name.
    mf              As String * MAXPATHLEN1     'master file name.
    ifi             As String * MAXPATHLEN1     'inverted file name.
    isoin           As String * MAXPATHLEN1     'import iso file name.
    isoout          As String * MAXPATHLEN1     'export iso file name.
    rec             As Long                     'number of RECSTRU shelves.
    trm             As Long                     'number of TRMSTRU shelves.
    filestatus      As Long                     'file Issue_status - bit mask.

End Type


Type IsisSrcHeader

    number          As Long                     'search number (start in 1).
    hits            As Long                     'total posting retrieved.
    recs            As Long                     'total records retrieved.
    segmentpostings As Long                     'number of hits.
    dbname          As String * MAXPATHLEN1     'data base name.
    booleanexpr     As String * SRC_EXPR_LENGTH1 'search expression.

End Type


Type IsisSrcHit

    Mfn             As Long                     'current hit mfn.
    tag             As Long                     'current hit tag.
    Occ             As Long                     'current hit occ.
    cnt             As Long                     'current hit cnt.

End Type


Type IsisSrcMfn

    Mfn             As Long                     'hit mfn component.

End Type


Type IsisTrmMfn

    Mfn             As Long                     'posting mfn component.

End Type


Type IsisTrmPosting

    posting         As Long                     'current posting order.
    Mfn             As Long                     'current posting pmfn.
    tag             As Long                     'current posting ptag.
    Occ             As Long                     'current posting pocc.
    cnt             As Long                     'current posting pcnt.

End Type


Type IsisTrmRead

    Key             As String * KEY_LENGTH1     'term key.

End Type



'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

'                            ISIS_DLL Error Codes

'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_


Global Const ZERO = 0

'--------------------------------------------------------------------------
'------------------ Data Base Errors --------------------------------------
'--------------------------------------------------------------------------

Global Const ERR_DBDELOCK = -101        ' Data Base access denied (data entry lock).
Global Const ERR_DBEWLOCK = -102        ' Data Base access denied (probably exclusive write lock).
Global Const ERR_DBMONOUSR = -103       ' Data Base access is single-user.
Global Const ERR_DBMULTUSR = -104       ' Data Base access is multi-user.


'--------------------------------------------------------------------------
'------------------ File Manipulation Erros -------------------------------
'--------------------------------------------------------------------------

Global Const ERR_FILECREATE = -201      ' File create error.
Global Const ERR_FILEDELETE = -202      ' File delete error.
Global Const ERR_FILEEMPTY = -203       ' File (empty).
Global Const ERR_FILEFLUSH = -204       ' File flush error.
Global Const ERR_FILEFMT = -205         ' File does not exist (fmt).
Global Const ERR_FILEFST = -206         ' File does not exist (fst).
Global Const ERR_FILEINVERT = -207      ' File does not exist (inverted).
Global Const ERR_FILEISO = -208         ' File does not exist (ISO).
Global Const ERR_FILEMASTER = -209      ' File does not exist (master).
Global Const ERR_FILEMISSING = -210     ' File missing.
Global Const ERR_FILEOPEN = -211        ' File open error.
Global Const ERR_FILEPFT = -212         ' File does not exist (pft).
Global Const ERR_FILEREAD = -213        ' File read error.
Global Const ERR_FILERENAME = -214      ' File rename error.
Global Const ERR_FILESTW = -215         ' File does not exist (stw).
Global Const ERR_FILEWRITE = -216       ' File write error.


'--------------------------------------------------------------------------
'------------------ Low Level Engine Errors -------------------------------
'--------------------------------------------------------------------------

Global Const ERR_LLCISISETRAP = -301    ' Cisis Low Level Error Trap.
Global Const ERR_LLISISETRAP = -302     ' Isis  Low Level Error Trap.


'--------------------------------------------------------------------------
'------------------ Memory Manipulation Errors ---------------------------
'--------------------------------------------------------------------------

Global Const ERR_MEMALLOCAT = -401      ' Memory Allocation Error.


'--------------------------------------------------------------------------
'------------------ Parameter Specification Errors ------------------------
'--------------------------------------------------------------------------

Global Const ERR_PARAPPHAND = -501      ' Invalid application handle.
Global Const ERR_PARFILNINV = -502      ' Invalid file name size.
Global Const ERR_PARFLDSYNT = -503      ' Syntax Error (field update).
Global Const ERR_PARFMTSYNT = -504      ' Syntax Error (format).
Global Const ERR_PARNULLPNT = -505      ' NULL pointer.
Global Const ERR_PARNULLSTR = -506      ' String with zero size.
Global Const ERR_PAROUTRANG = -507      ' Parameter out of range.
Global Const ERR_PARSPAHAND = -508      ' Invalid space handle.
Global Const ERR_PARSRCSYNT = -509      ' Syntax Error (search).
Global Const ERR_PARSUBFSPC = -510      ' Invalid subfield specification.
Global Const ERR_PARUPDSYNT = -511      ' Syntax Error (record update).


'--------------------------------------------------------------------------
'------------------ Record Errors -----------------------------------------
'--------------------------------------------------------------------------

Global Const ERR_RECEOF = -601          ' Record eof: found eof in data base.
Global Const ERR_RECLOCKED = -602       ' Record locked.
Global Const ERR_RECLOGIDEL = -603      ' Record logically deleted.
Global Const ERR_RECNOTNORM = -604      ' Record condition is not RCNORMAL.
Global Const ERR_RECPHYSDEL = -605      ' Record physically deleted.


'--------------------------------------------------------------------------
'------------------ Term Errors -------------------------------------------
'--------------------------------------------------------------------------

Global Const ERR_TRMEOF = -701          ' Term eof: found eof in data base.
Global Const ERR_TRMNEXT = -702         ' Term next: key not found.


'--------------------------------------------------------------------------
'------------------ Unexpected Errors -------------------------------------
'--------------------------------------------------------------------------

Global Const ERR_UNEXPECTED = -999      ' Unexpected Error.



'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

'                    IsisSpaHeader - filestatus

'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

'
'  ---------------------- File Issue_status ------------------------------
'
'  Máscara de bits indicando quais são os arquivos existentes.
'
'  00000000 00000000 00000000 00000000          0 = No open files.
'  00000000 00000000 00000000 00000001          1 = Master   *.mst
'  00000000 00000000 00000000 00000010          2 = Master   *.xrf
'  00000000 00000000 00000000 00000100          4 = Inverted *.cnt
'  00000000 00000000 00000000 00001000          8 = Inverted *.n01
'  00000000 00000000 00000000 00010000         16 = Inverted *.n02
'  00000000 00000000 00000000 00100000         32 = Inverted *.l01
'  00000000 00000000 00000000 01000000         64 = Inverted *.l02
'  00000000 00000000 00000000 10000000        128 = Inverted *.ifp

'  00000000 00000000 00000001 00000000        256 =          *.fst
'  00000000 00000000 00000010 00000000        512 =          *.pft
'  00000000 00000000 00000100 00000000       1024 =          *.pft (Cisis)
'  00000000 00000000 00001000 00000000       2048 =          *.fmt
'  00000000 00000000 00010000 00000000       4096 =          *.stw
'  00000000 00000000 00100000 00000000       8192 =          *.fdt
'  00000000 00000000 01000000 00000000      16384 = ISO in   *.iso
'  00000000 00000000 10000000 00000000      32738 = ISO out  *.iso

'  00000000 00000001 00000000 00000000      65536 = Cipar    *.par
'  00000000 00000010 00000000 00000000     131072 = Gizmo
'  00000000 00000100 00000000 00000000     262144 = Decode

'  00000001 00000000 00000000 00000000   16777216 =          *.any
