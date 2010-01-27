<?php
    $version = split ("\.", phpversion());
    if ( $version[0] > 4 || ($version[0] == 4 && $version[1] >= 1) ) {
        require_once($CONFIGURATION['COMMON']['PATH_CLASS_XSL_TRANSFORMER']."class.XSLTransformer41.php");
    }
    else {
        require_once($CONFIGURATION['COMMON']['PATH_CLASS_XSL_TRANSFORMER']."class.XSLTransformer40.php");
    }
?>