import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.utils import timezone

from .models import Internship, Application, Notification, Payment
from user_management.models import Student


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

    # Track applied and pending-payment internships for logged-in student
    applied_internship_ids = set()
    pending_payment_internship_ids = set()

    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            applied_internship_ids = set(
                Application.objects.filter(
                    student=student,
                    payment__status='Success'
                ).values_list('internship_id', flat=True)
            )
            pending_payment_internship_ids = set(
                Application.objects.filter(
                    student=student,
                    payment__status='Pending'
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
        'pending_payment_internship_ids': pending_payment_internship_ids,
        'today': today,
        'total_count': internships.count(),
    })


def internship_detail(request, id):
    """
    Detailed view of an internship posting, showing specifications,
    deadline status, and student application/payment state.
    """
    internship = get_object_or_404(Internship, id=id)
    today = timezone.now().date()
    is_expired = internship.application_deadline < today

    existing_application = None
    is_payment_pending = False
    is_payment_success = False

    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            existing_application = Application.objects.filter(
                student=student,
                internship=internship
            ).first()

            if existing_application and hasattr(existing_application, 'payment'):
                is_payment_pending = existing_application.payment.status == 'Pending'
                is_payment_success = existing_application.payment.status == 'Success'
        except Student.DoesNotExist:
            pass

    # Convert comma-separated skills to a list for badge rendering
    skills_list = [s.strip() for s in internship.skills_required.split(',') if s.strip()]

    return render(request, 'internships/internship_detail.html', {
        'internship': internship,
        'skills_list': skills_list,
        'is_expired': is_expired,
        'existing_application': existing_application,
        'already_applied': is_payment_success,
        'is_payment_pending': is_payment_pending,
        'today': today,
    })


@login_required
def apply_internship(request, id):
    """
    Handles application initialization and redirects to demo application fee payment.
    Ensures students who abandon payment can resume seamlessly.
    """
    internship = get_object_or_404(Internship, id=id)

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
        if hasattr(existing_application, 'payment') and existing_application.payment.status == 'Pending':
            messages.info(request, "You already started an application for this internship. Please complete your payment.")
            return redirect('payment_page', id=existing_application.id)
        else:
            messages.info(request, f"You have already applied for '{internship.title}'.")
            return redirect('my_applications')

    skills_list = [s.strip() for s in internship.skills_required.split(',') if s.strip()]

    # When student clicks Confirm Application
    if request.method == 'POST':
        # Create application in Pending review state
        application = Application.objects.create(
            student=student,
            internship=internship,
            status='Pending'
        )

        # Create corresponding pending fee payment
        Payment.objects.create(
            application=application,
            amount=500.00,
            status='Pending'
        )

        # Redirect to demo payment page
        return redirect('payment_page', id=application.id)

    return render(request, 'internships/apply_internship.html', {
        'internship': internship,
        'skills_list': skills_list,
        'student': student,
    })


@login_required
def payment_page(request, id):
    """
    Displays the demo payment gateway page with payment method options.
    Simulates secure payment and transitions application to submitted.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile required.")
        return redirect('student_dashboard')

    application = get_object_or_404(
        Application,
        id=id,
        student=student
    )

    payment = get_object_or_404(
        Payment,
        application=application
    )

    # If already paid, redirect straight to receipt
    if payment.status == 'Success':
        return redirect('payment_success', id=payment.id)

    if request.method == 'POST':
        selected_method = request.POST.get('payment_method', 'UPI / Online')

        # Generate unique transaction ID
        payment.transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        payment.payment_method = selected_method
        payment.status = 'Success'
        payment.paid_at = timezone.now()
        payment.save()

        # Send official confirmation notification
        Notification.objects.create(
            student=student,
            message=(
                f'Payment of ₹{payment.amount:.2f} for "{application.internship.title}" '
                f'at {application.internship.company_name} was successful. '
                f'(Txn ID: {payment.transaction_id}). Your application has been submitted.'
            )
        )

        messages.success(request, "Application fee payment completed successfully! Your application is now submitted.")
        return redirect('payment_success', id=payment.id)

    return render(request, 'internships/payment.html', {
        'application': application,
        'payment': payment,
        'internship': application.internship,
        'student': student,
    })


@login_required
def payment_success(request, id):
    """
    Displays the payment receipt and confirmation page.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile required.")
        return redirect('student_dashboard')

    payment = get_object_or_404(
        Payment,
        id=id,
        application__student=student,
        status='Success'
    )

    return render(request, 'internships/payment_success.html', {
        'payment': payment,
        'application': payment.application,
        'internship': payment.application.internship,
        'student': student,
    })


@login_required
def my_applications(request):
    """
    Displays submitted applications (with successful payment) as well as
    any pending payments requiring completion.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile required to view applications.")
        return redirect('student_dashboard')

    status_filter = request.GET.get('status', '').strip()

    # Completed & paid applications
    applications = Application.objects.filter(
        student=student,
        payment__status='Success'
    ).select_related('internship', 'payment').order_by('-applied_at')

    if status_filter:
        applications = applications.filter(status=status_filter)

    # Incomplete/unpaid applications
    pending_payment_apps = Application.objects.filter(
        student=student,
        payment__status='Pending'
    ).select_related('internship', 'payment').order_by('-applied_at')

    total_count = Application.objects.filter(
        student=student,
        payment__status='Success'
    ).count()

    return render(request, 'internships/my_applications.html', {
        'applications': applications,
        'pending_payment_apps': pending_payment_apps,
        'pending_payment_count': pending_payment_apps.count(),
        'status_filter': status_filter,
        'total_count': total_count,
    })


@login_required
def withdraw_application(request, id):
    """
    Allows a student to withdraw an application in Pending review status
    or cancel an unpaid pending application.
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
    except Exception:
        messages.error(request, "Unable to withdraw application.")

    return redirect('my_applications')