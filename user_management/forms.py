import os
import re
from django import forms
from django.contrib.auth.models import User
from .models import Student


def validate_full_name(name):
    """Validates full name for proper alphabetic characters and reasonable length."""
    name = (name or '').strip()
    if not name:
        raise forms.ValidationError("Full name is required.")
    if len(name) < 2:
        raise forms.ValidationError("Full name must be at least 2 characters long.")
    if len(name) > 100:
        raise forms.ValidationError("Full name cannot exceed 100 characters.")
    if not re.match(r"^[a-zA-Z\s\.\'\-]+$", name):
        raise forms.ValidationError("Full name must contain letters, spaces, dots, and hyphens only.")
    if not re.search(r"[a-zA-Z]", name):
        raise forms.ValidationError("Full name must contain alphabetic characters.")
    return name


def validate_phone_number(phone):
    """
    Validates phone number to strictly enforce a valid 10-digit Indian mobile number
    (starting with 6, 7, 8, or 9), automatically stripping country code (+91/0) and spaces.
    """
    phone = (phone or '').strip()
    if not phone:
        raise forms.ValidationError("Phone number is required.")
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    if cleaned.startswith('+91') and len(cleaned) == 13:
        cleaned = cleaned[3:]
    elif cleaned.startswith('91') and len(cleaned) == 12:
        cleaned = cleaned[2:]
    elif cleaned.startswith('0') and len(cleaned) == 11:
        cleaned = cleaned[1:]

    if not re.match(r'^[6-9][0-9]{9}$', cleaned):
        raise forms.ValidationError(
            "Please enter a valid 10-digit mobile number starting with 6, 7, 8, or 9 (e.g. 9876543210)."
        )
    return cleaned


def validate_resume_file(file_obj):
    """Validates uploaded resume extension (.pdf, .doc, .docx) and file size (max 5MB)."""
    if not file_obj:
        return None
    if hasattr(file_obj, 'name') and hasattr(file_obj, 'size'):
        ext = os.path.splitext(file_obj.name)[1].lower()
        allowed = ['.pdf', '.doc', '.docx']
        if ext not in allowed:
            raise forms.ValidationError(
                f"Unsupported file format '{ext}'. Only PDF, DOC, and DOCX files are allowed."
            )
        max_size_mb = 5
        if file_obj.size > max_size_mb * 1024 * 1024:
            raise forms.ValidationError(
                f"Resume file size must not exceed {max_size_mb} MB."
            )
        if file_obj.size == 0:
            raise forms.ValidationError(
                "The uploaded resume file is empty. Please upload a valid document."
            )
    return file_obj


class StudentForm(forms.ModelForm):
    """
    Registration form for new students of MEA Engineering College.
    Creates both the Django User and the Student profile with comprehensive field validation.
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
            'placeholder': 'Enter password (min 8 characters)'
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
                'placeholder': 'e.g. 9876543210'
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
        if len(reg_no) < 5 or len(reg_no) > 30:
            raise forms.ValidationError('Registration number must be between 5 and 30 characters (e.g. MEA22MCA001).')
        if not re.match(r'^[A-Z0-9\-_/]+$', reg_no):
            raise forms.ValidationError('Registration number must contain only uppercase letters, numbers, and hyphens.')
        if Student.objects.filter(registration_number__iexact=reg_no).exists():
            raise forms.ValidationError('This registration number is already registered.')
        return reg_no

    def clean_name(self):
        return validate_full_name(self.cleaned_data.get('name'))

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise forms.ValidationError('Email address is required.')
        if Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email address is already associated with an account.')
        return email

    def clean_phone(self):
        return validate_phone_number(self.cleaned_data.get('phone'))

    def clean_course(self):
        course = (self.cleaned_data.get('course') or '').strip()
        valid_courses = [c[0] for c in Student.COURSE_CHOICES]
        if not course or course not in valid_courses:
            raise forms.ValidationError('Please select a valid department / course from the list.')
        return course

    def clean_resume(self):
        return validate_resume_file(self.cleaned_data.get('resume'))

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        if not username:
            raise forms.ValidationError('Username is required.')
        if len(username) < 3 or len(username) > 150:
            raise forms.ValidationError('Username must be between 3 and 150 characters.')
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            raise forms.ValidationError('Username can only contain letters, numbers, underscores, dots, or hyphens.')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Password is required.')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
            raise forms.ValidationError('Passwords do not match.')

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
                'placeholder': 'e.g. 9876543210'
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
        if len(reg_no) < 5 or len(reg_no) > 30:
            raise forms.ValidationError('Registration number must be between 5 and 30 characters (e.g. MEA22MCA001).')
        if not re.match(r'^[A-Z0-9\-_/]+$', reg_no):
            raise forms.ValidationError('Registration number must contain only uppercase letters, numbers, and hyphens.')

        qs = Student.objects.filter(registration_number__iexact=reg_no)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('This registration number is already in use by another student.')

        return reg_no

    def clean_name(self):
        return validate_full_name(self.cleaned_data.get('name'))

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise forms.ValidationError('Email address is required.')

        qs = Student.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('This email address is already in use by another student.')

        user_pk = self.instance.user_id if self.instance else None
        u_qs = User.objects.filter(email__iexact=email)
        if user_pk:
            u_qs = u_qs.exclude(pk=user_pk)
        if u_qs.exists():
            raise forms.ValidationError('This email address is already in use by another account.')

        return email

    def clean_phone(self):
        return validate_phone_number(self.cleaned_data.get('phone'))

    def clean_course(self):
        course = (self.cleaned_data.get('course') or '').strip()
        valid_courses = [c[0] for c in Student.COURSE_CHOICES]
        if not course or course not in valid_courses:
            raise forms.ValidationError('Please select a valid department / course from the list.')
        return course

    def clean_resume(self):
        return validate_resume_file(self.cleaned_data.get('resume'))