from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models

from .forms import StudentForm, StudentProfileEditForm
from .models import Student
from internships.models import Internship, Application, Notification


def home(request):
    """
    Landing page showcasing InternHub features, stats, and portal access.
    """
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    total_internships = Internship.objects.count()
    total_students = Student.objects.count()
    recent_internships = Internship.objects.order_by('-created_at')[:3]

    return render(request, 'user_management/home.html', {
        'total_internships': total_internships,
        'total_students': total_students,
        'recent_internships': recent_internships,
    })


def student_register(request):
    """
    Registers a new student account and associated Django user.
    """
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=username,
                password=password,
                email=form.cleaned_data['email']
            )

            student = form.save(commit=False)
            student.user = user
            student.save()

            # Welcome notification
            Notification.objects.create(
                student=student,
                message=f"Welcome to InternHub, {student.name}! Start exploring available internships."
            )

            # Automatically log the student in
            login(request, user)
            messages.success(request, f"Welcome to InternHub, {student.name}! Your account has been created.")
            return redirect('student_dashboard')
    else:
        form = StudentForm()

    return render(request, 'user_management/student_register.html', {
        'form': form
    })


def student_success(request):
    return render(request, 'user_management/student_success.html')


def student_login(request):
    """
    Authenticates students and handles next-url redirects.
    """
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    next_url = request.GET.get('next') or request.POST.get('next') or 'student_dashboard'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'user_management/student_login.html', {
        'next': next_url
    })


def student_logout(request):
    """
    Logs out the user and redirects to login page.
    """
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('student_login')


@login_required
def student_dashboard(request):
    """
    Student dashboard displaying comprehensive application metrics,
    recent applications, and latest notifications.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        if request.user.is_staff:
            return redirect('/admin/')
        messages.error(request, "Student profile not found. Please contact administration.")
        return redirect('student_logout')

    applications = Application.objects.filter(student=student)

    # Metric counts
    total_applications = applications.count()
    pending_applications = applications.filter(status='Pending').count()
    under_review_applications = applications.filter(status='Under Review').count()
    shortlisted_applications = applications.filter(status='Shortlisted').count()
    selected_applications = applications.filter(status='Selected').count()
    rejected_applications = applications.filter(status='Rejected').count()

    # Recent items
    recent_applications = applications.select_related('internship').order_by('-applied_at')[:5]
    recent_notifications = Notification.objects.filter(student=student).order_by('-created_at')[:5]

    return render(request, 'user_management/student_dashboard.html', {
        'student': student,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'under_review_applications': under_review_applications,
        'shortlisted_applications': shortlisted_applications,
        'selected_applications': selected_applications,
        'rejected_applications': rejected_applications,
        'recent_applications': recent_applications,
        'recent_notifications': recent_notifications,
    })


@login_required
def student_profile(request, id=None):
    """
    View student profile details and statistics.
    Ensures students view their own profile.
    """
    try:
        current_student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('student_dashboard')

    # Security check: if ID provided doesn't match current user and not staff
    if id and id != current_student.id and not request.user.is_staff:
        messages.warning(request, "You can only view your own profile.")
        student = current_student
    elif id:
        student = get_object_or_404(Student, id=id)
    else:
        student = current_student

    applications_count = Application.objects.filter(student=student).count()
    selected_count = Application.objects.filter(student=student, status='Selected').count()

    return render(request, 'user_management/student_profile.html', {
        'student': student,
        'applications_count': applications_count,
        'selected_count': selected_count,
    })


@login_required
def student_edit(request, id=None):
    """
    Edit student profile information using StudentProfileEditForm.
    Restricted to the logged-in student for their own record.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = StudentProfileEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            # Sync email with user model
            request.user.email = student.email
            request.user.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('student_profile', id=student.id)
    else:
        form = StudentProfileEditForm(instance=student)

    return render(request, 'user_management/student_edit.html', {
        'form': form,
        'student': student
    })


@login_required
def student_notifications(request):
    """
    View notifications for the logged in student with unread indicators.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('student_dashboard')

    filter_type = request.GET.get('filter', 'all')

    notifications = Notification.objects.filter(student=student).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()

    if filter_type == 'unread':
        notifications = notifications.filter(is_read=False)

    return render(request, 'user_management/student_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'filter_type': filter_type,
    })


@login_required
def mark_notification_read(request, id):
    """
    Marks a single notification as read.
    """
    try:
        student = Student.objects.get(user=request.user)
        notification = get_object_or_404(Notification, id=id, student=student)
        notification.is_read = True
        notification.save()
    except Exception:
        pass

    return redirect('student_notifications')


@login_required
def mark_all_notifications_read(request):
    """
    Marks all notifications for the logged-in student as read.
    """
    try:
        student = Student.objects.get(user=request.user)
        Notification.objects.filter(student=student, is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read.")
    except Exception:
        pass

    return redirect('student_notifications')


@login_required
def delete_notification(request, id):
    """
    Deletes a specific notification.
    """
    try:
        student = Student.objects.get(user=request.user)
        notification = get_object_or_404(Notification, id=id, student=student)
        notification.delete()
        messages.success(request, "Notification deleted.")
    except Exception:
        pass

    return redirect('student_notifications')


@login_required
def student_list(request):
    """
    Staff-only view of registered students.
    """
    if not request.user.is_staff:
        messages.error(request, "Access restricted to administrators.")
        return redirect('student_dashboard')

    students = Student.objects.all().order_by('-created_at')
    return render(request, 'user_management/student_list.html', {
        'students': students
    })


@login_required
def student_delete(request, id):
    """
    Staff-only deletion of a student.
    """
    if not request.user.is_staff:
        messages.error(request, "Access restricted to administrators.")
        return redirect('student_dashboard')

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, f"Student {student.name} deleted.")
        return redirect('student_list')

    return render(request, 'user_management/student_delete.html', {
        'student': student
    })