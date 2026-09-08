from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.utils import timezone

from .models import Internship, Application, Notification
from user_management.models import Student


def internship_list(request):
    """
    Lists available internships with keyword search, location filtering,
    and applied status indicators for logged-in students.
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

    # Track applied internships for logged in student
    applied_internship_ids = set()
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            applied_internship_ids = set(
                Application.objects.filter(student=student).values_list('internship_id', flat=True)
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


def internship_detail(request, id):
    """
    Detailed view of an internship posting, showing all specifications,
    deadline status, and student application state.
    """
    internship = get_object_or_404(Internship, id=id)
    today = timezone.now().date()
    is_expired = internship.application_deadline < today

    existing_application = None
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            existing_application = Application.objects.filter(
                student=student,
                internship=internship
            ).first()
        except Student.DoesNotExist:
            pass

    # Convert comma-separated skills to a list for badge rendering
    skills_list = [s.strip() for s in internship.skills_required.split(',') if s.strip()]

    return render(request, 'internships/internship_detail.html', {
        'internship': internship,
        'skills_list': skills_list,
        'is_expired': is_expired,
        'existing_application': existing_application,
        'already_applied': existing_application is not None,
        'today': today,
    })


@login_required
def apply_internship(request, id):
    """
    Handles application submission for an internship.
    Enforces deadline validation and duplicate prevention.
    """
    internship = get_object_or_404(Internship, id=id)

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Only registered students can apply for internships.")
        return redirect('student_dashboard')

    today = timezone.now().date()
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

    # Process application
    if request.method == 'POST':
        application = Application.objects.create(
            student=student,
            internship=internship,
            status='Pending'
        )

        # Dispatch notification
        Notification.objects.create(
            student=student,
            message=f'Your application for "{internship.title}" at {internship.company_name} has been submitted successfully.'
        )

        messages.success(request, f"Application for '{internship.title}' submitted successfully!")
        return redirect('my_applications')

    skills_list = [s.strip() for s in internship.skills_required.split(',') if s.strip()]

    return render(request, 'internships/apply_internship.html', {
        'internship': internship,
        'skills_list': skills_list,
        'student': student,
    })


@login_required
def my_applications(request):
    """
    Displays all submitted applications with status badges,
    timeline information, and withdrawal capabilities.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile required to view applications.")
        return redirect('student_dashboard')

    status_filter = request.GET.get('status', '').strip()

    applications = Application.objects.filter(student=student).select_related('internship').order_by('-applied_at')

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
    Allows a student to withdraw a pending application.
    """
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
    except Exception as e:
        messages.error(request, "Unable to withdraw application.")

    return redirect('my_applications')