# email_sender/forms.py
from django import forms

class EmailUploadForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Subject"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label="Message"
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        label="Upload Excel File"
    )
