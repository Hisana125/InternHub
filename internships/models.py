from django.db import models
from user_management.models import Student
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class Internship(models.Model):
    title = models.CharField(max_length=200)

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='internships'
    )

    company_name = models.CharField(max_length=200)

    description = models.TextField()
    location = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    stipend = models.CharField(max_length=100)
    skills_required = models.CharField(max_length=300)
    application_deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'internship'],
                name='unique_student_internship_application'
            )
        ]


class Notification(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.message}"