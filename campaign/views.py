# email_sender/views.py
import openpyxl
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailUploadForm

def send_bulk_email(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            file = request.FILES['file']

            # Load the uploaded Excel file
            wb = openpyxl.load_workbook(file)
            sheet = wb.active

            # Collect all email addresses from the first column
            email_list = []
            for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
                email = row[0]
                if email:
                    email_list.append(email)

            # Send email to all collected email addresses
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, email_list)
                return render(request, 'success.html', {'emails': email_list})
            except Exception as e:
                return render(request, 'error.html', {'error': str(e)})

    else:
        form = EmailUploadForm()

    return render(request, 'email_form.html', {'form': form})
