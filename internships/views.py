import uuid
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import models, transaction
from django.db.models import Count, Q
from django.utils import timezone

from .models import Internship, Application, Notification, Company
from .forms import CompanyRegistrationForm, InternshipForm, CompanyProfileEditForm
from user_management.models import Student


def company_required(view_func):
    """
    Decorator ensuring that only authenticated users with a registered
    Company profile can access the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('student_login')}?next={request.path}")
        if not hasattr(request.user, 'company'):
            messages.error(request, "Access restricted to registered company accounts.")
            if hasattr(request.user, 'student'):
                return redirect('student_dashboard')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def company_register(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'company'):
            return redirect('company_dashboard')
        elif hasattr(request.user, 'student'):
            return redirect('student_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=form.cleaned_data['email']
                )

                company = form.save(commit=False)
                company.user = user
                company.save()

            login(request, user)

            messages.success(
                request,
                f"Welcome to InternHub, {company.company_name}! "
                "Your company account has been created."
            )

            return redirect('company_dashboard')

    else:
        form = CompanyRegistrationForm()

    return render(
        request,
        'internships/company_register.html',
        {'form': form}
    )


@company_required
def company_dashboard(request):
    company = request.user.company

    internships = Internship.objects.filter(
        company=company
    ).annotate(
        applicants_count=Count('application')
    ).order_by('-created_at')

    today = timezone.now().date()
    total_postings = internships.count()
    active_postings = internships.filter(application_deadline__gte=today).count()
    total_applicants = Application.objects.filter(
        internship__company=company
    ).count()
    selected_applicants = Application.objects.filter(
        internship__company=company,
        status='Selected'
    ).count()

    return render(
        request,
        'internships/company_dashboard.html',
        {
            'company': company,
            'internships': internships,
            'total_postings': total_postings,
            'active_postings': active_postings,
            'total_applicants': total_applicants,
            'selected_applicants': selected_applicants,
            'today': today,
        }
    )


@company_required
def company_post_internship(request):
    company = request.user.company

    if request.method == 'POST':
        form = InternshipForm(request.POST)

        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = company
            internship.company_name = company.company_name
            internship.save()

            messages.success(
                request,
                f"Internship '{internship.title}' has been posted successfully!"
            )
            return redirect('company_dashboard')

    else:
        form = InternshipForm()

    return render(
        request,
        'internships/company_post_internship.html',
        {
            'form': form,
            'company': company,
            'is_edit': False,
        }
    )


@company_required
def company_edit_internship(request, id):
    company = request.user.company
    internship = get_object_or_404(Internship, id=id, company=company)

    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = company
            internship.company_name = company.company_name
            internship.save()

            messages.success(
                request,
                f"Internship '{internship.title}' has been updated successfully!"
            )
            return redirect('company_dashboard')
    else:
        form = InternshipForm(instance=internship)

    return render(
        request,
        'internships/company_post_internship.html',
        {
            'form': form,
            'company': company,
            'internship': internship,
            'is_edit': True,
        }
    )


@company_required
def company_delete_internship(request, id):
    company = request.user.company
    internship = get_object_or_404(Internship, id=id, company=company)

    if request.method == 'POST':
        title = internship.title
        internship.delete()
        messages.success(request, f"Internship '{title}' was deleted successfully.")
    else:
        messages.warning(request, "Deletion requires confirmation.")

    return redirect('company_dashboard')


@company_required
def company_profile_edit(request):
    company = request.user.company

    if request.method == 'POST':
        form = CompanyProfileEditForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            request.user.email = company.email
            request.user.save()

            messages.success(request, "Company profile updated successfully!")
            return redirect('company_dashboard')
    else:
        form = CompanyProfileEditForm(instance=company)

    return render(
        request,
        'internships/company_profile_edit.html',
        {
            'form': form,
            'company': company,
        }
    )

def internship_list(request):
    """
    Lists available internships with keyword search, location filtering,
    and applied/payment status indicators for logged-in students.
    """
    query = request.GET.get('q', '').strip()
    location_filter = request.GET.get('location', '').strip()

    internships = Internship.objects.all().order_by('-created_at')

    # Keyword search across title, company, location, and skills
    if query:
        internships = internships.filter(
            models.Q(title__icontains=query) |
            models.Q(company_name__icontains=query) |
            models.Q(location__icontains=query) |
            models.Q(skills_required__icontains=query)
        )

    # Location filter
    if location_filter:
        internships = internships.filter(location__iexact=location_filter)

    # Distinct locations for dropdown filter
    locations = Internship.objects.values_list('location', flat=True).distinct()

    # Track applied internships for logged-in student
    applied_internship_ids = set()

    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            applied_internship_ids = set(
                Application.objects.filter(
                    student=student
                ).values_list('internship_id', flat=True)
            )
        except Student.DoesNotExist:
            pass

    today = timezone.now().date()

    return render(request, 'internships/internship_list.html', {
        'internships': internships,
        'query': query,
        'location_filter': location_filter,
        'locations': locations,
        'applied_internship_ids': applied_internship_ids,
        'today': today,
        'total_count': internships.count(),
    })


@company_required
def company_view_applicants(request, id):
    company = request.user.company

    internship = get_object_or_404(
        Internship,
        id=id,
        company=company
    )

    applications = Application.objects.filter(
        internship=internship
    ).select_related(
        'student',
        'internship'
    ).order_by('-applied_at')

    return render(
        request,
        'internships/company_view_applicants.html',
        {
            'company': company,
            'internship': internship,
            'applications': applications,
        }
    )


@company_required
def company_update_application_status(request, id):
    # Only accept form submissions
    if request.method != 'POST':
        return redirect('company_dashboard')

    company = request.user.company

    # Find an application belonging to this company's internship
    application = get_object_or_404(
        Application,
        id=id,
        internship__company=company
    )

    new_status = request.POST.get('status', '').strip()

    # Accept only statuses defined in the Application model
    valid_statuses = dict(Application.STATUS_CHOICES)

    if new_status not in valid_statuses:
        messages.error(request, "Please select a valid application status.")
        return redirect(
            'company_view_applicants',
            id=application.internship.id
        )

    old_status = application.status

    if new_status == old_status:
        messages.info(request, "The application already has this status.")
    else:
        application.status = new_status
        application.save(update_fields=['status'])

        # Notify the student about the status change
        Notification.objects.create(
            student=application.student,
            message=(
                f"Your application for '{application.internship.title}' "
                f"at {company.company_name} has been updated from "
                f"'{old_status}' to '{new_status}'."
            )
        )

        messages.success(
            request,
            f"Application status updated to '{new_status}'. "
            "The student has been notified."
        )

    return redirect(
        'company_view_applicants',
        id=application.internship.id
    )


def internship_detail(request, id):
    """
    Detailed view of an internship posting, showing specifications,
    deadline status, and student application/payment state.
    """
    internship = get_object_or_404(Internship, id=id)
    today = timezone.now().date()
    is_expired = internship.application_deadline < today

    existing_application = None
    already_applied = False
    is_owner_company = False
    is_company_user = False

    if request.user.is_authenticated:
        if hasattr(request.user, 'company'):
            is_company_user = True
            if internship.company == request.user.company:
                is_owner_company = True
        else:
            try:
                student = Student.objects.get(user=request.user)
                existing_application = Application.objects.filter(
                    student=student,
                    internship=internship
                ).first()
                already_applied = existing_application is not None
            except Student.DoesNotExist:
                pass

    # Convert comma-separated skills to a list for badge rendering
    skills_list = [s.strip() for s in internship.skills_required.split(',') if s.strip()]

    return render(request, 'internships/internship_detail.html', {
        'internship': internship,
        'skills_list': skills_list,
        'is_expired': is_expired,
        'existing_application': existing_application,
        'already_applied': already_applied,
        'is_owner_company': is_owner_company,
        'is_company_user': is_company_user,
        'today': today,
    })


@login_required
def apply_internship(request, id):
    """
    Handles 100% free application submission for MEA Engineering College students.
    Directly creates the application and notifies the student.
    """
    internship = get_object_or_404(Internship, id=id)

    if hasattr(request.user, 'company'):
        messages.warning(request, "Company accounts cannot apply for internships.")
        return redirect('internship_detail', id=internship.id)

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Only registered students can apply for internships.")
        return redirect('student_dashboard')

    today = timezone.now().date()

    # Check application deadline
    if internship.application_deadline < today:
        messages.error(request, f"The application deadline for '{internship.title}' has passed.")
        return redirect('internship_detail', id=internship.id)

    # Check for existing application
    existing_application = Application.objects.filter(
        student=student,
        internship=internship
    ).first()

    if existing_application:
        messages.info(request, f"You have already applied for '{internship.title}'.")
        return redirect('my_applications')

    skills_list = [s.strip() for s in internship.skills_required.split(',') if s.strip()]

    # When student clicks Confirm Application
    if request.method == 'POST':
        application = Application.objects.create(
            student=student,
            internship=internship,
            status='Pending'
        )

        Notification.objects.create(
            student=student,
            message=(
                f'Your application for "{internship.title}" at {internship.company_name} '
                f'has been submitted successfully.'
            )
        )

        messages.success(
            request,
            f'Your application for "{internship.title}" has been submitted successfully!'
        )
        return redirect('my_applications')

    return render(request, 'internships/apply_internship.html', {
        'internship': internship,
        'skills_list': skills_list,
        'student': student,
    })


@login_required
def my_applications(request):
    """
    Displays all submitted applications for the logged-in student.
    """
    if hasattr(request.user, 'company'):
        return redirect('company_dashboard')

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile required to view applications.")
        return redirect('student_dashboard')

    status_filter = request.GET.get('status', '').strip()

    applications = Application.objects.filter(
        student=student
    ).select_related('internship').order_by('-applied_at')

    if status_filter:
        applications = applications.filter(status=status_filter)

    total_count = Application.objects.filter(student=student).count()

    return render(request, 'internships/my_applications.html', {
        'applications': applications,
        'status_filter': status_filter,
        'total_count': total_count,
    })


@login_required
def withdraw_application(request, id):
    """
    Allows a student to withdraw an application in Pending review status
    or cancel an unpaid pending application.
    """
    if hasattr(request.user, 'company'):
        return redirect('company_dashboard')

    try:
        student = Student.objects.get(user=request.user)
        application = get_object_or_404(Application, id=id, student=student)

        if application.status == 'Pending':
            internship_title = application.internship.title
            application.delete()

            Notification.objects.create(
                student=student,
                message=f'Your application for "{internship_title}" was withdrawn.'
            )

            messages.info(request, f"Your application for '{internship_title}' has been withdrawn.")
        else:
            messages.error(request, "Only pending applications can be withdrawn.")
    except Exception:
        messages.error(request, "Unable to withdraw application.")

    return redirect('my_applications')