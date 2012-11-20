from pyPdf import PdfFileWriter, PdfFileReader
import os

#Esta es la marca de agua!!!!!!
nombre_plantilla = 'watermark.pdf'

from sys import argv

nombre_pdf_salida = argv[2]
filename = argv[1]

#Generamos los streams de entrada y salida
output = PdfFileWriter()

#Obtenemos los ficheros del directorio que queremos convertir en un solo
watermark = PdfFileReader(file(nombre_plantilla, "rb"))

input1 = PdfFileReader(file(filename,"rb"))
#print 'Anyadimos : ' + str(f)
#Obtenemos el numero de paginas del documento
for np in range(0,input1.getNumPages()):
#Anyadimos pagina
    page = input1.getPage(np)
    page.mergePage(watermark.getPage(0))
    output.addPage(page)






outputStream = file(nombre_pdf_salida, "wb")
output.write(outputStream)
print( "-----------------------------------------------------------------")
print("Hemos generado el fichero : " + nombre_pdf_salida)
print( "-----------------------------------------------------------------")

