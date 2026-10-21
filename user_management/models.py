from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    COURSE_CHOICES = [
        ('MCA', 'Master of Computer Applications (MCA)'),
        ('B.Tech CSE', 'B.Tech Computer Science & Engineering'),
        ('B.Tech AI & DS', 'B.Tech Artificial Intelligence & Data Science'),
        ('B.Tech IT', 'B.Tech Information Technology'),
        ('B.Tech ECE', 'B.Tech Electronics & Communication Engineering'),
        ('B.Tech EEE', 'B.Tech Electrical & Electronics Engineering'),
        ('B.Tech ME', 'B.Tech Mechanical Engineering'),
        ('B.Tech CE', 'B.Tech Civil Engineering'),
        ('B.Tech RA', 'B.Tech Robotics & Automation'),
        ('M.Tech CSE', 'M.Tech Computer Science & Engineering'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    registration_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        help_text="College Registration / Roll Number (e.g. MEA22MCA001)"
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.registration_number:
            return f"{self.name} ({self.registration_number})"
        return self.name