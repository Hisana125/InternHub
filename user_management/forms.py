from django import forms
from django.contrib.auth.models import User
from .models import Student


class StudentForm(forms.ModelForm):
    """
    Registration form for new students of MEA Engineering College.
    Creates both the Django User and the Student profile.
    """

    registration_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. MEA22MCA001 / MEA21CS045'
        })
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = Student
        fields = [
            'registration_number',
            'name',
            'email',
            'phone',
            'course',
            'resume'
        ]

        widgets = {
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. MEA22MCA001 / MEA21CS045'
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. yourname@meaec.edu.in'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +91 9876543210'
            }),

            'course': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[('', '-- Select Department / Course --')] + Student.COURSE_CHOICES),

            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }

    def clean_registration_number(self):
        reg_no = (self.cleaned_data.get('registration_number') or '').strip().upper()
        if not reg_no:
            raise forms.ValidationError('Registration number is required.')

        if Student.objects.filter(registration_number__iexact=reg_no).exists():
            raise forms.ValidationError('This registration number is already registered.')

        return reg_no


    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                'Passwords do not match.'
            )

        return cleaned_data


class StudentProfileEditForm(forms.ModelForm):
    """
    Edit form for updating student profile information.
    Does not require or modify password/username.
    """

    class Meta:
        model = Student

        fields = [
            'registration_number',
            'name',
            'email',
            'phone',
            'course',
            'resume'
        ]

        widgets = {
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. MEA22MCA001'
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'course': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[('', '-- Select Department / Course --')] + Student.COURSE_CHOICES),

            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }

    def clean_registration_number(self):
        reg_no = (self.cleaned_data.get('registration_number') or '').strip().upper()
        if not reg_no:
            raise forms.ValidationError('Registration number is required.')

        qs = Student.objects.filter(registration_number__iexact=reg_no)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('This registration number is already in use by another student.')

        return reg_no