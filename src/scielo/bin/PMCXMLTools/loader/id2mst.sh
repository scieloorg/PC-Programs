cisis_path=$1
idfile=$2
db=$3

$cisis_path/id2i $idfile create=temp 
$cisis_path/mx temp now -all append=$db 

