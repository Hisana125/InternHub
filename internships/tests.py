from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from user_management.models import Student
from internships.models import Internship, Application, Notification, Company
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

    def test_successful_free_application(self):
        # 1. Apply creates application directly with Pending status
        response = self.client.post(reverse('apply_internship', args=[self.internship.id]), follow=True)
        self.assertEqual(response.status_code, 200)

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

        # Apply again - should redirect to my_applications without creating duplicate
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


class CompanyWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.today = timezone.now().date()

        # Create a company user
        self.company_user = User.objects.create_user(
            username='innovatetech',
            password='CompanyPassword123',
            email='contact@innovate.com'
        )
        self.company = Company.objects.create(
            user=self.company_user,
            company_name='InnovateTech Solutions',
            email='contact@innovate.com',
            phone='9876543210',
            address='Infopark, Kochi',
            website='https://innovatetech.com',
            description='IT & Product development'
        )

        # Create a student user
        self.student_user = User.objects.create_user(
            username='student1',
            password='StudentPassword123',
            email='student1@test.com'
        )
        self.student = Student.objects.create(
            user=self.student_user,
            name='First Student',
            email='student1@test.com',
            phone='9123456780',
            course='MCA'
        )

        # Create an internship posted by company
        self.internship = Internship.objects.create(
            company=self.company,
            company_name=self.company.company_name,
            title='Backend Python Developer',
            description='Work on microservices with Django and FastAPI.',
            location='Kochi, Kerala',
            duration='3 Months',
            stipend='₹15,000 / month',
            skills_required='Python, Django, SQL',
            application_deadline=self.today + timedelta(days=20)
        )

    def test_company_registration_success(self):
        response = self.client.post(reverse('company_register'), {
            'company_name': 'NextGen Corp',
            'email': 'hr@nextgen.com',
            'phone': '9988776655',
            'address': 'Cyberpark, Kozhikode',
            'website': 'https://nextgen.com',
            'description': 'AI and Cloud Solutions',
            'username': 'nextgencorp',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Company.objects.filter(company_name='NextGen Corp').exists())
        self.assertTrue(User.objects.filter(username='nextgencorp').exists())
        self.assertRedirects(response, reverse('company_dashboard'))

    def test_company_login_redirects_to_company_dashboard(self):
        response = self.client.post(reverse('student_login'), {
            'username': 'innovatetech',
            'password': 'CompanyPassword123'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('company_dashboard'))
        self.assertContains(response, 'InnovateTech Solutions')

    def test_student_cannot_access_company_dashboard(self):
        self.client.login(username='student1', password='StudentPassword123')
        response = self.client.get(reverse('company_dashboard'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_company_cannot_apply_for_internship(self):
        self.client.login(username='innovatetech', password='CompanyPassword123')
        response = self.client.post(reverse('apply_internship', args=[self.internship.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Application.objects.filter(internship=self.internship).exists())

    def test_company_post_internship(self):
        self.client.login(username='innovatetech', password='CompanyPassword123')
        response = self.client.post(reverse('company_post_internship'), {
            'title': 'Frontend Vue.js Intern',
            'description': 'Build responsive interfaces using Vue 3.',
            'location': 'Kochi, Kerala',
            'duration': '3 Months',
            'stipend': '₹12,000 / month',
            'skills_required': 'Vue.js, JavaScript, CSS3',
            'application_deadline': self.today + timedelta(days=25),
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        new_internship = Internship.objects.filter(title='Frontend Vue.js Intern').first()
        self.assertIsNotNone(new_internship)
        self.assertEqual(new_internship.company, self.company)
        self.assertEqual(new_internship.company_name, self.company.company_name)

    def test_past_deadline_validation_on_post_internship(self):
        self.client.login(username='innovatetech', password='CompanyPassword123')
        past_date = self.today - timedelta(days=5)
        response = self.client.post(reverse('company_post_internship'), {
            'title': 'Invalid Past Internship',
            'description': 'Description with invalid date.',
            'location': 'Kochi',
            'duration': '1 Month',
            'stipend': '₹5,000',
            'skills_required': 'Testing',
            'application_deadline': past_date,
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Internship.objects.filter(title='Invalid Past Internship').exists())
        self.assertFormError(response, 'form', 'application_deadline', 'Application deadline cannot be in the past.')

    def test_company_view_all_applicants(self):
        Application.objects.create(
            student=self.student,
            internship=self.internship,
            status='Pending'
        )

        second_user = User.objects.create_user(username='secondstudent', password='Password123')
        second_student = Student.objects.create(
            user=second_user,
            registration_number='MEA22MCA098',
            name='Second Student',
            email='second@test.com',
            phone='9999999999',
            course='MCA'
        )
        Application.objects.create(
            student=second_student,
            internship=self.internship,
            status='Pending'
        )

        self.client.login(username='innovatetech', password='CompanyPassword123')
        response = self.client.get(reverse('company_view_applicants', args=[self.internship.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First Student')
        self.assertContains(response, 'Second Student')

    def test_company_update_applicant_status_dispatches_notification(self):
        app = Application.objects.create(
            student=self.student,
            internship=self.internship,
            status='Pending'
        )

        self.client.login(username='innovatetech', password='CompanyPassword123')
        response = self.client.post(
            reverse('company_update_application_status', args=[app.id]),
            {'status': 'Shortlisted'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.status, 'Shortlisted')

        # Verify student received notification
        notif = Notification.objects.filter(
            student=self.student,
            message__icontains='Shortlisted'
        ).first()
        self.assertIsNotNone(notif)


from internships.forms import CompanyRegistrationForm, InternshipForm, CompanyProfileEditForm


class CompanyAndInternshipFieldValidationTests(TestCase):
    def setUp(self):
        self.today = timezone.now().date()
        self.valid_company_data = {
            'company_name': 'ValidTech Solutions',
            'username': 'validtech',
            'email': 'hr@validtech.com',
            'phone': '+91 9876543210',
            'address': 'Infopark Phase 2, Kakkanad, Kochi',
            'website': 'https://validtech.com',
            'description': 'IT services and AI development',
            'password': 'SecureCompanyPass123!',
            'confirm_password': 'SecureCompanyPass123!',
        }

        self.valid_internship_data = {
            'title': 'Full Stack Django Developer',
            'description': 'Develop scalable backend microservices and responsive frontends.',
            'location': 'Kochi, Kerala',
            'duration': '6 Months',
            'stipend': '₹18,000 / month',
            'skills_required': 'Python, Django, PostgreSQL, HTML5',
            'application_deadline': self.today + timedelta(days=25),
        }

    def test_valid_company_form_passes(self):
        form = CompanyRegistrationForm(data=self.valid_company_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['phone'], '9876543210')
        self.assertEqual(form.cleaned_data['email'], 'hr@validtech.com')

    def test_short_or_invalid_company_name_rejected(self):
        data = self.valid_company_data.copy()
        data['company_name'] = 'A'  # Too short
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

        data['company_name'] = '###$$$'  # No alphanumeric chars
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_duplicate_company_name_rejected(self):
        user = User.objects.create_user(username='origcompany', password='Pass1234Password')
        Company.objects.create(
            user=user,
            company_name='ValidTech Solutions',
            email='orig@validtech.com',
            phone='9876543210',
            address='Kochi'
        )
        data = self.valid_company_data.copy()
        data['username'] = 'anotheruser'
        data['email'] = 'unique@validtech.com'
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_invalid_company_phone_rejected(self):
        data = self.valid_company_data.copy()
        data['phone'] = '123'  # Too short
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

        data['phone'] = '1234567890'  # Starts with 1
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_short_company_address_rejected(self):
        data = self.valid_company_data.copy()
        data['address'] = 'USA'  # Less than 5 chars
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('address', form.errors)

    def test_website_url_auto_scheme_and_validation(self):
        # Accepts valid URLs
        data = self.valid_company_data.copy()
        data['website'] = 'https://www.mycompany.org'
        form = CompanyRegistrationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['website'], 'https://www.mycompany.org')

        # Invalid URL format rejected
        data['website'] = 'not-a-valid-url-@@@'
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)

    def test_company_password_validation(self):
        data = self.valid_company_data.copy()
        data['password'] = 'short'
        data['confirm_password'] = 'short'
        form = CompanyRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_valid_internship_form_passes(self):
        form = InternshipForm(data=self.valid_internship_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['title'], 'Full Stack Django Developer')

    def test_short_internship_title_rejected(self):
        data = self.valid_internship_data.copy()
        data['title'] = 'AI'  # Less than 3 chars
        form = InternshipForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_short_internship_description_rejected(self):
        data = self.valid_internship_data.copy()
        data['description'] = 'Short text'  # Less than 15 chars
        form = InternshipForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_past_application_deadline_rejected(self):
        data = self.valid_internship_data.copy()
        data['application_deadline'] = self.today - timedelta(days=1)
        form = InternshipForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('application_deadline', form.errors)

    def test_skills_required_formatting(self):
        data = self.valid_internship_data.copy()
        data['skills_required'] = ' Python  ,  Django ,   PostgreSQL  '
        form = InternshipForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['skills_required'], 'Python, Django, PostgreSQL')

