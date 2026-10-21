from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Company, Internship


class CompanyRegistrationForm(forms.ModelForm):

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
                'placeholder': '+91 9876543210'
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

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(
            username__iexact=username
        ).exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if (
            password
            and confirm_password
            and password != confirm_password
        ):
            raise forms.ValidationError(
                'Passwords do not match.'
            )

        return cleaned_data
class InternshipForm(forms.ModelForm):

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
                'placeholder': 'e.g. 3 months'
            }),

            'stipend': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. ₹10,000 per month'
            }),

            'skills_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python, Django, MySQL'
            }),

            'application_deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')
        if deadline and deadline < timezone.now().date():
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
                'placeholder': '+91 9876543210'
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