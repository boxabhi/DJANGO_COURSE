from datetime import datetime
from django.template.loader import get_template
from django.conf import settings
import pdfkit
import requests
import base64

def generateOrderId(index):
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    return f"OD{year}{month}{day}{index.zfill(5)}"



def generateOrderPdf(instance,data):
    dynamic_directory_name = f"public/static/pdfs/{instance.order_id}.pdf"
    template_name = "invoice"

    options  = {
        'no-outline' : None,
        'page-size' : 'A4',
        'margin-top' : '0.2in',
        'margin-bottom' : '0.2in',
        'margin-left' : '0.2in',
        'margin-right' : '0.2in',
    } 
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    template = get_template(f"pdfs/{template_name}.html")
    content = template.render(data)
    exact_file_path = f"{settings.BASE_DIR}/{dynamic_directory_name}"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(content, exact_file_path, options = options, configuration=config)




def getImageBase64(image_url):
    response = requests.get(image_url)
    print(response)
    if response.status_code == 200:
        base64_data  = base64.b64encode(response.content)
        return base64_data.decode('utf-8')

