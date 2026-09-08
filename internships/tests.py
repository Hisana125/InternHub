from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from user_management.models import Student
from internships.models import Internship, Application, Notification
from internships.admin import ApplicationAdmin
from django.contrib.admin.sites import AdminSite


class InternshipListingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.today = timezone.now().date()
        self.internship1 = Internship.objects.create(
            title='Django Backend Developer',
            company_name='TechCorp',
            description='Build web apps using Django and Python.',
            location='Kochi',
            duration='3 Months',
            stipend='₹15,000 / month',
            skills_required='Python, Django, PostgreSQL',
            application_deadline=self.today + timedelta(days=30)
        )
        self.internship2 = Internship.objects.create(
            title='Frontend React Developer',
            company_name='WebWorks',
            description='Build interfaces with React.',
            location='Bangalore',
            duration='6 Months',
            stipend='₹20,000 / month',
            skills_required='JavaScript, React, CSS',
            application_deadline=self.today + timedelta(days=20)
        )

    def test_internship_list_view(self):
        response = self.client.get(reverse('internship_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Backend Developer')
        self.assertContains(response, 'Frontend React Developer')

    def test_internship_search_filter(self):
        # Search for Django
        response = self.client.get(reverse('internship_list') + '?q=Django')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Backend Developer')
        self.assertNotContains(response, 'Frontend React Developer')

    def test_internship_location_filter(self):
        # Filter by Bangalore
        response = self.client.get(reverse('internship_list') + '?location=Bangalore')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Frontend React Developer')
        self.assertNotContains(response, 'Django Backend Developer')

    def test_internship_detail_view(self):
        response = self.client.get(reverse('internship_detail', args=[self.internship1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Backend Developer')
        self.assertContains(response, 'TechCorp')
        self.assertContains(response, 'Kochi')
        self.assertContains(response, '3 Months')
        self.assertContains(response, 'Python')


class ApplicationWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.today = timezone.now().date()
        self.user = User.objects.create_user(username='applicant', password='Password123')
        self.student = Student.objects.create(
            user=self.user,
            name='Test Applicant',
            email='applicant@test.com',
            phone='9876543210',
            course='MCA'
        )
        self.internship = Internship.objects.create(
            title='Cloud Engineer Intern',
            company_name='CloudSys',
            description='Cloud automation with AWS.',
            location='Kochi',
            duration='3 Months',
            stipend='₹15,000 / month',
            skills_required='AWS, Docker, Linux',
            application_deadline=self.today + timedelta(days=30)
        )
        self.expired_internship = Internship.objects.create(
            title='Expired Opportunity',
            company_name='OldCorp',
            description='Old opportunity.',
            location='Kochi',
            duration='3 Months',
            stipend='₹10,000',
            skills_required='General',
            application_deadline=self.today - timedelta(days=5)
        )
        self.client.login(username='applicant', password='Password123')

    def test_successful_application(self):
        response = self.client.post(reverse('apply_internship', args=[self.internship.id]), follow=True)
        self.assertEqual(response.status_code, 200)

        # Check Application created with 'Pending' status
        app = Application.objects.filter(student=self.student, internship=self.internship).first()
        self.assertIsNotNone(app)
        self.assertEqual(app.status, 'Pending')

        # Check Notification dispatched to student
        self.assertTrue(Notification.objects.filter(
            student=self.student,
            message__icontains=self.internship.title
        ).exists())

    def test_duplicate_application_prevention(self):
        # Apply once
        self.client.post(reverse('apply_internship', args=[self.internship.id]))
        self.assertEqual(Application.objects.filter(student=self.student, internship=self.internship).count(), 1)

        # Apply again - should redirect without creating duplicate
        response = self.client.post(reverse('apply_internship', args=[self.internship.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.filter(student=self.student, internship=self.internship).count(), 1)

    def test_expired_deadline_application_blocked(self):
        response = self.client.post(reverse('apply_internship', args=[self.expired_internship.id]), follow=True)
        self.assertFalse(Application.objects.filter(student=self.student, internship=self.expired_internship).exists())

    def test_withdraw_pending_application(self):
        app = Application.objects.create(
            student=self.student,
            internship=self.internship,
            status='Pending'
        )
        response = self.client.get(reverse('withdraw_application', args=[app.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Application.objects.filter(id=app.id).exists())


class AdminActionTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = ApplicationAdmin(Application, self.site)
        self.today = timezone.now().date()
        self.user = User.objects.create_user(username='appuser', password='Password123')
        self.student = Student.objects.create(
            user=self.user,
            name='App Student',
            email='app@test.com',
            phone='1234567890',
            course='MCA'
        )
        self.internship = Internship.objects.create(
            title='AI Research Intern',
            company_name='OpenAI Lab',
            description='Deep learning research.',
            location='Remote',
            duration='6 Months',
            stipend='₹25,000',
            skills_required='PyTorch, NLP',
            application_deadline=self.today + timedelta(days=30)
        )
        self.app = Application.objects.create(
            student=self.student,
            internship=self.internship,
            status='Pending'
        )

    def test_admin_save_model_creates_notification_on_status_change(self):
        # Change status from Pending to Shortlisted
        self.app.status = 'Shortlisted'
        request = type('Request', (), {'user': self.user})()
        self.admin.save_model(request, self.app, form=None, change=True)

        notif = Notification.objects.filter(
            student=self.student,
            message__icontains='Shortlisted'
        ).first()
        self.assertIsNotNone(notif)
