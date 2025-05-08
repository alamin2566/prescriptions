from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import HeaderFooter
from django.http import JsonResponse
from .models import TemplateData


import pdfkit
from .models import Prescription
from datetime import datetime, date
from weasyprint import HTML
import io
# Homepage
def Homepage(request):
    return render(request, 'home.html')

# Signup view
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Passwords do not match!")
        else:
            user = User.objects.create_user(username=uname, email=email, password=pass1)
            user.save()
            return redirect('login')
    return render(request, 'signup.html')

# Login view
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect!")
    return render(request, 'login.html')

# Logout view
def LogoutPage(request):
    logout(request)
    return redirect('login')

# Prescription form and PDF generation
# Helper functions to safely parse input
def prescription_view(request):
    
    if request.method == 'POST':
        data = {key: request.POST.get(key, '').strip() for key in request.POST.keys()}
        try:
            # Parse the date or use today's date if empty
            if data.get('date'):
                parsed_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            else:
                parsed_date = date.today()

            prescription = Prescription.objects.create(
                name=data['name'],
                age=int(data['age']) if data['age'].isdigit() else 0,
                sex=data['sex'],
                address=data['address'],
                mobile=data['mobile'],
                reg_no=data['reg_no'],
                appointment=data['appointment'],
                date=parsed_date,
                disease=data.get('disease', ''),
                cc=data.get('c_c', ''),
                oe=data.get('oe', ''),
                ix=data.get('ix', ''),
                drug_history=data.get('drug_history', ''),

                blood_pressure = data.get('blood_pressure', ''),
                pulse = data.get('pulse', ''),
                temperature = data.get('temperature', ''),
                heart = data.get('heart_exam', ''),
                lungs = data.get('lungs_exam', ''),
                abdomen = data.get('abdomen_exam', ''),
                anaemia = data.get('anaemia', ''),
                jaundice = data.get('jaundice', ''),
                cyanosis = data.get('cyanosis', ''),
                oedema = data.get('oedema', ''),
                medicines = data.get('prescription_content', '')
            )

            doctor = {
                'english_name': 'Arif Jaman',
                'bangla_name': 'আরিফ জামান',
                'english_qualification': 'MBBS',
                'bangla_qualification': 'এমবিবিএস',
                'english_specialization': 'General Physician',
                'bangla_specialization': 'জেনারেল ফিজিশিয়ান',
                'bmdc_reg_no': 'A-137696'
            }
           
            

            html = render_to_string('receipt_template.html', {
                'prescription': prescription,
                'doctor': doctor
            }, request=request)

            pdf_file = HTML(string=html).write_pdf()

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="prescription.pdf"'
            return response

            # # ✅ Correct executable path
            # #path_to_wkhtmltopdf = r'C:\wkhtmltox\bin\wkhtmltopdf.exe'
            # #config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

            # # Render HTML and convert to PDF
            # #receipt_html = render_to_string('receipt_template.html', {'prescription': prescription})
            # # pdf = pdfkit.from_string(receipt_html, False, configuration=config)
            # html = render_to_string('receipt_template.html', 
            #           {'prescription': prescription,
            #           'doctor': doctor},
            #           request=request).encode('utf-8')
            # #html = render_to_string('receipt_template.html', {'prescription': prescription})

            # #return render(request, 'receipt_template.html',  {'prescription': prescription,
            # #          'doctor': doctor})

            # # result = io.BytesIO()
            # # pisa_status = pisa.CreatePDF(html, dest=result)
            # result = io.BytesIO()
            # pdf = pisa.CreatePDF(html, dest=result, encoding='UTF-8')

            # if pdf.err:
            #     return HttpResponse("PDF generation failed")

            # response = HttpResponse(result.getvalue(), content_type='application/pdf')
            # response['Content-Disposition'] = 'inline; filename="prescription.pdf"'
            # return response

        except Exception as e:
            return HttpResponse(f"Error creating prescription: {str(e)}", status=400)

    return render(request, 'prescription_form.html')
# View to generate PDF receipt for a specific prescription
def prescription_receipt(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    path_to_wkhtmltopdf = r'C:\wkhtmltox\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    receipt_html = render_to_string('receipt_template.html', {'prescription': prescription})
    pdf = pdfkit.from_string(receipt_html, False, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="receipt.pdf"'
    return response

# View to list all prescriptions
def prescription_list(request):
    prescriptions = Prescription.objects.all().order_by('-date')  # Or filter per user if needed
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})

#header
def header_edit_view(request):
    header, created = HeaderFooter.objects.get_or_create(id=1)  # Only 1 config used

    if request.method == "POST":
        header.background_color = request.POST.get('bg_color', '#FFFFFF')
        header.footer_text = request.POST.get('footer_text', '')
        header.show_barcode = request.POST.get('barcode') == 'yes'
        header.save()
        return redirect('header_edit')

    return render(request, 'header_edit.html', {'header': header})
from django.http import JsonResponse

from django.shortcuts import render
from django.http import JsonResponse
from .models import TemplateData

def get_templates(request):
    query = request.GET.get('q', '').lower()
    template_type = request.GET.get('type')

    templates = TemplateData.objects.filter(type=template_type)

    if query:
        results = [t.content for t in templates if query in t.content.lower()]
    else:
        results = []

    return JsonResponse({'results': results})
