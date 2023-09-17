from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json
def createPDF(location, json, destination):
    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #writeBox(can, infos["address0"], 103, 113, 100, 50)
    for k in json.keys():
        if (k == "policyNumber"):
            writeBox(can=can, fontSize=14, str=json[k], x=102, y=98, width=100,height=400,length=200)
        elif (k == "address0"):
            writeBox(can=can, fontSize=10, str=json[k], x=48, y=151, width=100, height=400, length=100)
        elif (k == "address1"):
            writeBox(can=can, fontSize=10, str=json[k], x=48, y=162, width=100, height=400, length=100)
        elif (k == "address2"):
            writeBox(can=can, fontSize=10, str=json[k], x=48, y=173, width=100, height=400, length=100)
        elif (k == "address3"):
            writeBox(can=can, fontSize=10, str=json[k], x=48, y=184, width=100, height=400, length=100)
        elif (k == "content"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=410, width=100, height=400, length=60)
        elif (k == "personal"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=421, width=100, height=400, length=60)
        elif (k == "annual"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=432, width=100, height=400, length=60)
        elif (k == "total"):
            writeBox(can=can, fontSize=10, str=json[k], x=530, y=465, width=100, height=400, length=60)
        elif (k == "date"):
            writeBox(can=can, fontSize=10, str=json[k], x=155, y=311, width=100, height=400, length=60)
        elif (k == "startdate"):
            writeBox(can=can, fontSize=10, str=json[k], x=155, y=343, width=100, height=400, length=60)
        elif (k == "enddate"):
            writeBox(can=can, fontSize=10, str=json[k], x=155, y=354, width=100, height=400, length=60)
        else:
            print("not recognised: " + str(k))
    can.showPage()
    can.save()
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # Read your existing PDF
    existing_pdf = PdfReader(open(location, "rb"))
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
def getPdf(jsonFile):
    personalCostInsurance = 0
    for item in jsonFile["StartupAssets"]:
        if item["Category"] == "Furniture":
            personalCostInsurance += 1
        elif item["Category"] == "Electronics":
            personalCostInsurance += 2
        elif item["Category"] == "Networking Equipment":
            personalCostInsurance += 1
        elif item["Category"] == "Security":
            personalCostInsurance += 1
        elif item["Category"] == "Office Supplies":
            personalCostInsurance += 1
        elif item["Category"] == "Furniture":
            personalCostInsurance += 3
        elif item["Category"] == "Appliances":
            personalCostInsurance += 2
    jsonFile["personal"] = str(personalCostInsurance)
    jsonFile["total"] = str(personalCostInsurance + int(jsonFile["annual"]) + int(jsonFile["content"]))
    createPDF("files/Household insurance Minimum incl PI.pdf", jsonFile, "output.pdf")
def testModification():
    jsonFile = {}
    jsonFile["policyNumber"] = "0123456789" # can be created automatically
    jsonFile["address0"] = "Mrs."
    jsonFile["address1"] = "Helen Hinderway"
    jsonFile["address2"] = "Hindenstr."
    jsonFile["address3"] = "70203 Zurich"
    jsonFile["content"] = "30"
    jsonFile["annual"] = "70"
    jsonFile["total"] = "180"
    jsonFile["date"] = "17.09.2023"
    jsonFile["startdate"] = "17.09.2023"
    jsonFile["enddate"] = "16.09.2024"
    jsonFile["StartupAssets"] = []
    jsonFile["StartupAssets"].append({"Category":"Furniture", "Item":"Long Table"})
    jsonFile["StartupAssets"].append({"Category":"Furniture", "Item":"Two Ergonomic Chairs"})
    jsonFile["StartupAssets"].append({"Category": "Electronics", "Item": "Two Laptops"})
    jsonFile["StartupAssets"].append({"Category": "Electronics", "Item": "Two External Monitors"})
    jsonFile["StartupAssets"].append({"Category": "Networking Equipment", "Item": "Server Rack"})
    jsonFile["StartupAssets"].append({"Category": "Security", "Item": "Lockable Metal Cage"})
    jsonFile["StartupAssets"].append({"Category": "Office Supplies", "Item": "Whiteboard"})
    jsonFile["StartupAssets"].append({"Category": "Furniture", "Item": "Filing Cabinet"})
    jsonFile["StartupAssets"].append({"Category": "Appliances", "Item": "Espresso Machine"})
    getPdf(jsonFile)
if __name__ == "__main__":
    testModification()
