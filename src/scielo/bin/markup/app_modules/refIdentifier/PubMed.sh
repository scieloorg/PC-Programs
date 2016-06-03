# argumento1 nome do arquivo com as marcacoes
# argumento2 nome do arquivo de saida
java -DLucene_Path=db -cp .:Marcador.jar:dom4j-1.6.1.jar:FOLLibrary.jar:Lucene.jar:lucene-core-2.3.1.jar:zeus.jar RefBib.PubMedCentral -infile:$1 -outfile:$2
