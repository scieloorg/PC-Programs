#This sample uses two third part modules for Python,
#pyPdf & ReportLab to achieve creating and placing
#watermark text at angle on an existing PDF file.
#This example was produced with Python 2.7
#See http://pybrary.net/pyPdf for more informaton about pyPdf.
#See http://www.reportlab.com for more information about ReportLab. 

#Import the needed external modules and functions from pyPdf and reportlab.
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas

#Use reportlab to create a PDF that will be used
#as a watermark on another PDF.
c= canvas.Canvas("watermark.pdf")
c.setFont("Courier", 60)
#This next setting with make the text of our
#watermark gray, nice touch for a watermark.
c.setFillGray(0.5,0.5)
#Set up our watermark document. Our watermark
#will be rotated 45 degrees from the direction
#of our underlying document.
c.saveState()
c.translate(500,100)
c.rotate(45)
c.drawCentredString(0, 0, "A WATERMARK!")
c.drawCentredString(0, 300, "A WATERMARK!")
c.drawCentredString(0, 600, "A WATERMARK!")
c.restoreState()
c.save() 

#Read in the PDF that will have the PDF applied to it.
output = PdfFileWriter()
input1 = PdfFileReader(file("original_pdf.pdf", "rb")) 

#Just to demo this function from pyPdf.
#If the PDF has a title, this will print it out.
print "title = %s" % (input1.getDocumentInfo().title)

#Open up the orgininal PDF.
page1 = input1.getPage(0)

#Read in the file created above by ReportLab for our watermark.
watermark = PdfFileReader(file("watermark.pdf", "rb"))
#Apply the watermark by merging the two PDF files.
page1.mergePage(watermark.getPage(0))
#Send the resultant PDF to the output stream.
output.addPage(page1)

#Just to demo this function from pyPdf.
#Return the number of pages in the watermarked PDF.
print "watermarked_pdf.pdf has %s pages." % input1.getNumPages()

#write the output of our new, watermarked PDF.
outputStream = file("watermarked_pdf.pdf", "wb")
output.write(outputStream)
outputStream.close()