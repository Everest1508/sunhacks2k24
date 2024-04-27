from django import forms

class UploadForm(forms.Form):
    job_description = forms.FileField(label='Upload Job Description')
    resume = forms.FileField(label='Upload Resume')
