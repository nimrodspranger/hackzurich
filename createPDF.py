import shutil
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
def test(location, reference, destination):
    shutil.copyfile(location, destination)
    # create a new PDF file
    #pdf = Canvas(destination)

    # add some text
    #pdf.drawString(100, 750, "Welcome to ReportLab!")

    # save the PDF file
    #pdf.save()
def test2(location, reference, destination):
    reader = PdfReader(location)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    print(text)

def createPDF(location, json, destination):
    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #writeBox(can, infos["address0"], 103, 113, 100, 50)
    for k in json.keys():
        if (k == "policyNumber"):
            writeBox(can=can, fontSize=14, str=json[k], x=102, y=98, width=100,height=400,length=200)
        elif (k == "annual"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=410, width=100, height=400, length=60)
        elif (k == "personal"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=421, width=100, height=400, length=60)
        elif (k == "content"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=432, width=100, height=400, length=60)
        elif (k == "total"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=465, width=100, height=400, length=60)
        else:
            print("not recognised: " + str(k))
    can.showPage()
    can.save()
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # Read your existing PDF
    existing_pdf = PdfReader(open(location, "rb"))
    print("height and width")
    print(existing_pdf.pages[0].mediabox.height)
    print(existing_pdf.pages[0].mediabox.width)
    output = PdfWriter()
    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # Finally, write "output" to a real file
    outputStream = open(destination, "wb")
    output.write(outputStream)
    outputStream.close()
def writeBox(can, fontSize, str, x, y, width, height, length):
    can.setFont('Helvetica-Bold', fontSize)
    can.setFillColor("white")
    can.setStrokeColor("white")
    can.rect(x, 841.9 - y - fontSize, length, fontSize, 1, 1)
    can.setStrokeColor("black")
    can.setFillColor("black")
    can.drawString(x, 841.9 - y - fontSize, str)
def getPdf(json):
    createPDF("files/Household insurance Minimum incl PI.pdf", json, "output.pdf")
def testModification():
    json = {}
    json["policyNumber"] = "0123456789"
    json["annual"] = "50"
    json["personal"] = "60"
    json["content"] = "70"
    json["total"] = "180"
    getPdf(json)
if __name__ == "__main__":
    testModification()