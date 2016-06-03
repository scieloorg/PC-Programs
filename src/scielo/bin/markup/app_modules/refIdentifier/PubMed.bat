@REM argumento1 nome do arquivo com as marcacoes
@REM argumento2 nome do arquivo de saida

set LOCAL_PATH=%4
echo parametro1 %1
echo parametro2 %2
set lucene=%LOCAL_PATH%/lucene-core-2.3.2.jar

del %3
@java -DLucene_Path=%LOCAL_PATH%/db -cp %LOCAL_PATH%;%LOCAL_PATH%/Marcador.jar;%LOCAL_PATH%/dom4j-1.6.1.jar;%LOCAL_PATH%/FOLLibrary.jar;%LOCAL_PATH%/Lucene.jar;%lucene%;%LOCAL_PATH%/zeus.jar RefBib.PubMedCentral -infile:%1 -outfile:%2
copy %2 %3
