import re
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Company, Internship


def validate_company_phone(phone):
    """
    Validates company phone number to strictly enforce a valid 10-digit Indian phone number
    (starting with 6, 7, 8, or 9), automatically stripping country code (+91/0) and spaces.
    """
    phone = (phone or '').strip()
    if not phone:
        raise forms.ValidationError("Contact phone number is required.")
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    if cleaned.startswith('+91') and len(cleaned) == 13:
        cleaned = cleaned[3:]
    elif cleaned.startswith('91') and len(cleaned) == 12:
        cleaned = cleaned[2:]
    elif cleaned.startswith('0') and len(cleaned) == 11:
        cleaned = cleaned[1:]

    if not re.match(r'^[6-9][0-9]{9}$', cleaned):
        raise forms.ValidationError(
            "Please enter a valid 10-digit phone number starting with 6, 7, 8, or 9 (e.g. 9876543210)."
        )
    return cleaned


def validate_company_website(website):
    """Validates website URL format and automatically ensures scheme is present."""
    website = (website or '').strip()
    if not website:
        return ""
    if not re.match(r'^https?://', website, re.IGNORECASE):
        website = 'https://' + website
    url_validator = forms.URLField().clean
    try:
        url_validator(website)
    except forms.ValidationError:
        raise forms.ValidationError("Please enter a valid website URL (e.g. https://www.example.com).")
    return website


class CompanyRegistrationForm(forms.ModelForm):
    """
    Registration form for employer and recruiting partner companies.
    Creates both the Django User and Company profile with strict validation.
    """

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter company username'
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
        model = Company
        fields = [
            'company_name',
            'email',
            'phone',
            'address',
            'website',
            'description'
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'company@example.com'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 9876543210'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company address',
                'rows': 3
            }),

            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your company and industry focus',
                'rows': 4
            }),
        }

    def clean_company_name(self):
        name = (self.cleaned_data.get('company_name') or '').strip()
        if not name:
            raise forms.ValidationError("Company name is required.")
        if len(name) < 2 or len(name) > 200:
            raise forms.ValidationError("Company name must be between 2 and 200 characters.")
        if not re.search(r'[a-zA-Z0-9]', name):
            raise forms.ValidationError("Company name must contain letters or numbers.")
        if Company.objects.filter(company_name__iexact=name).exists():
            raise forms.ValidationError("A company with this name is already registered.")
        return name

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

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise forms.ValidationError("Official email address is required.")
        if Company.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already registered to a company.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already associated with an account.")
        return email

    def clean_phone(self):
        return validate_company_phone(self.cleaned_data.get('phone'))

    def clean_address(self):
        address = (self.cleaned_data.get('address') or '').strip()
        if not address:
            raise forms.ValidationError("Headquarters / office address is required.")
        if len(address) < 5:
            raise forms.ValidationError("Please provide a complete address (at least 5 characters).")
        return address

    def clean_website(self):
        return validate_company_website(self.cleaned_data.get('website'))

    def clean_description(self):
        return (self.cleaned_data.get('description') or '').strip()

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required.")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class InternshipForm(forms.ModelForm):
    """
    Form for posting and updating internship opportunities.
    """

    class Meta:
        model = Internship
        fields = [
            'title',
            'description',
            'location',
            'duration',
            'stipend',
            'skills_required',
            'application_deadline'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python Developer Intern'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the internship role and responsibilities',
                'rows': 5
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Kochi, Kerala / Remote'
            }),

            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 3 Months, 6 Months'
            }),

            'stipend': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. ₹15,000 / month, ₹10,000 / month, or Unpaid'
            }),

            'skills_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python, Django, MySQL, REST APIs'
            }),

            'application_deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise forms.ValidationError("Internship title is required.")
        if len(title) < 3 or len(title) > 200:
            raise forms.ValidationError("Internship title must be between 3 and 200 characters.")
        if not re.search(r'[a-zA-Z]', title):
            raise forms.ValidationError("Internship title must contain alphabetic characters.")
        return title

    def clean_description(self):
        desc = (self.cleaned_data.get('description') or '').strip()
        if not desc:
            raise forms.ValidationError("Internship description is required.")
        if len(desc) < 15:
            raise forms.ValidationError(
                "Description must be at least 15 characters to provide sufficient details for applicants."
            )
        return desc

    def clean_location(self):
        location = (self.cleaned_data.get('location') or '').strip()
        if not location:
            raise forms.ValidationError("Location is required.")
        if len(location) < 2 or len(location) > 100:
            raise forms.ValidationError("Location must be between 2 and 100 characters (e.g. Kochi, Kerala or Remote).")
        return location

    def clean_duration(self):
        duration = (self.cleaned_data.get('duration') or '').strip()
        if not duration:
            raise forms.ValidationError("Duration is required.")
        if len(duration) < 2 or len(duration) > 100:
            raise forms.ValidationError("Duration must be between 2 and 100 characters (e.g. 3 Months, 6 Months).")
        return duration

    def clean_stipend(self):
        stipend = (self.cleaned_data.get('stipend') or '').strip()
        if not stipend:
            raise forms.ValidationError("Stipend is required.")
        if len(stipend) < 2 or len(stipend) > 100:
            raise forms.ValidationError("Stipend must be between 2 and 100 characters (e.g. ₹15,000 / month or Unpaid).")
        return stipend

    def clean_skills_required(self):
        skills = (self.cleaned_data.get('skills_required') or '').strip()
        if not skills:
            raise forms.ValidationError("Required skills are required.")
        # Clean and format comma-separated skill list
        skill_tags = [s.strip() for s in skills.split(',') if s.strip()]
        if not skill_tags:
            raise forms.ValidationError("Please provide at least one valid technical skill.")
        return ', '.join(skill_tags)

    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')
        if not deadline:
            raise forms.ValidationError("Application deadline is required.")
        if deadline < timezone.now().date():
            raise forms.ValidationError("Application deadline cannot be in the past.")
        return deadline


class CompanyProfileEditForm(forms.ModelForm):
    """
    Form for updating company profile details.
    """
    class Meta:
        model = Company
        fields = [
            'company_name',
            'email',
            'phone',
            'address',
            'website',
            'description'
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'company@example.com'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 9876543210'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company address',
                'rows': 3
            }),

            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your company',
                'rows': 4
            }),
        }

    def clean_company_name(self):
        name = (self.cleaned_data.get('company_name') or '').strip()
        if not name:
            raise forms.ValidationError("Company name is required.")
        if len(name) < 2 or len(name) > 200:
            raise forms.ValidationError("Company name must be between 2 and 200 characters.")
        if not re.search(r'[a-zA-Z0-9]', name):
            raise forms.ValidationError("Company name must contain letters or numbers.")

        qs = Company.objects.filter(company_name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A company with this name is already registered.")

        return name

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise forms.ValidationError("Official email address is required.")

        qs = Company.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email address is already registered to another company.")

        user_pk = self.instance.user_id if self.instance else None
        u_qs = User.objects.filter(email__iexact=email)
        if user_pk:
            u_qs = u_qs.exclude(pk=user_pk)
        if u_qs.exists():
            raise forms.ValidationError("This email address is already in use by another account.")

        return email

    def clean_phone(self):
        return validate_company_phone(self.cleaned_data.get('phone'))

    def clean_address(self):
        address = (self.cleaned_data.get('address') or '').strip()
        if not address:
            raise forms.ValidationError("Office address is required.")
        if len(address) < 5:
            raise forms.ValidationError("Please provide a complete address (at least 5 characters).")
        return address

    def clean_website(self):
        return validate_company_website(self.cleaned_data.get('website'))

    def clean_description(self):
        return (self.cleaned_data.get('description') or '').strip()