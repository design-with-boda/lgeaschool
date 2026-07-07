from django import forms
from .models import ContactMessage, AdmissionInquiry


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
        }


class AdmissionInquiryForm(forms.ModelForm):
    class Meta:
        model = AdmissionInquiry
        fields = ['child_name', 'date_of_birth', 'gender', 'class_applying',
                  'parent_name', 'parent_phone', 'parent_email', 'address', 'additional_info']
        widgets = {
            'child_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'class_applying': forms.Select(attrs={'class': 'form-select'},
                choices=[
                    ('', 'Select Class'),
                    ('Nursery 1', 'Nursery 1'),
                    ('Nursery 2', 'Nursery 2'),
                    ('Primary 1', 'Primary 1'),
                    ('Primary 2', 'Primary 2'),
                    ('Primary 3', 'Primary 3'),
                    ('Primary 4', 'Primary 4'),
                    ('Primary 5', 'Primary 5'),
                    ('Primary 6', 'Primary 6'),
                ]),
            'parent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
