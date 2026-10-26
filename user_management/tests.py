from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user_management.models import Student
from internships.models import Notification


class StudentRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_registration(self):
        data = {
            'registration_number': 'MEA22MCA099',
            'name': 'Test Student',
            'email': 'student@test.com',
            'phone': '9876543210',
            'course': 'MCA',
            'username': 'teststudent',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
        }
        response = self.client.post(reverse('student_register'), data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify User and Student created
        user = User.objects.filter(username='teststudent').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('SecurePassword123!'))

        student = Student.objects.filter(user=user).first()
        self.assertIsNotNone(student)
        self.assertEqual(student.registration_number, 'MEA22MCA099')
        self.assertEqual(student.name, 'Test Student')
        self.assertEqual(student.course, 'MCA')

        # Verify welcome notification
        self.assertTrue(Notification.objects.filter(student=student).exists())

    def test_registration_duplicate_registration_number(self):
        Student.objects.create(
            registration_number='MEA22MCA001',
            name='Existing Reg Student',
            email='existingreg@test.com',
            phone='1112223334',
            course='MCA'
        )
        data = {
            'registration_number': 'MEA22MCA001',
            'name': 'Duplicate Reg Student',
            'email': 'dup2@test.com',
            'phone': '9876543210',
            'course': 'MCA',
            'username': 'dupreguser',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
        }
        response = self.client.post(reverse('student_register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='dupreguser').exists())

    def test_registration_password_mismatch(self):
        data = {
            'registration_number': 'MEA22MCA088',
            'name': 'Mismatch Student',
            'email': 'mismatch@test.com',
            'phone': '9876543210',
            'course': 'MCA',
            'username': 'mismatchuser',
            'password': 'Password123',
            'confirm_password': 'DifferentPassword456',
        }
        response = self.client.post(reverse('student_register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_registration_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='password123')
        data = {
            'registration_number': 'MEA22MCA077',
            'name': 'Duplicate User',
            'email': 'dup@test.com',
            'phone': '9876543210',
            'course': 'MCA',
            'username': 'existinguser',
            'password': 'Password123',
            'confirm_password': 'Password123',
        }
        response = self.client.post(reverse('student_register'), data)
        self.assertEqual(response.status_code, 200)
        # Should not create duplicate
        self.assertEqual(User.objects.filter(username='existinguser').count(), 1)


class StudentAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='loginuser', password='Password123')
        self.student = Student.objects.create(
            user=self.user,
            registration_number='MEA22MCA001',
            name='Login User',
            email='login@test.com',
            phone='1234567890',
            course='MCA'
        )

    def test_successful_login(self):
        response = self.client.post(reverse('student_login'), {
            'username': 'loginuser',
            'password': 'Password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_failed_login(self):
        response = self.client.post(reverse('student_login'), {
            'username': 'loginuser',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(username='loginuser', password='Password123')
        response = self.client.get(reverse('student_logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)


class StudentProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='profileuser', password='Password123')
        self.student = Student.objects.create(
            user=self.user,
            registration_number='MEA22MCA010',
            name='Profile User',
            email='profile@test.com',
            phone='9876543210',
            course='MCA'
        )
        self.client.login(username='profileuser', password='Password123')

    def test_profile_view(self):
        response = self.client.get(reverse('student_profile', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile User')
        self.assertContains(response, 'MCA')
        self.assertContains(response, 'MEA22MCA010')

    def test_profile_edit(self):
        # Test editing profile without requiring password
        response = self.client.post(reverse('student_edit_self'), {
            'registration_number': 'MEA22MCA010',
            'name': 'Updated Profile Name',
            'email': 'updated@test.com',
            'phone': '9999999999',
            'course': 'M.Tech CSE'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        self.student.refresh_from_db()
        self.assertEqual(self.student.registration_number, 'MEA22MCA010')
        self.assertEqual(self.student.name, 'Updated Profile Name')
        self.assertEqual(self.student.email, 'updated@test.com')
        self.assertEqual(self.student.phone, '9999999999')
        self.assertEqual(self.student.course, 'M.Tech CSE')


class NotificationWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='notifuser', password='Password123')
        self.student = Student.objects.create(
            user=self.user,
            registration_number='MEA22MCA050',
            name='Notif User',
            email='notif@test.com',
            phone='1234567890',
            course='MCA'
        )
        self.client.login(username='notifuser', password='Password123')
        self.notif1 = Notification.objects.create(
            student=self.student,
            message="Notification 1",
            is_read=False
        )
        self.notif2 = Notification.objects.create(
            student=self.student,
            message="Notification 2",
            is_read=False
        )

    def test_notification_list_and_unread_count(self):
        response = self.client.get(reverse('student_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['unread_count'], 2)

    def test_mark_single_notification_read(self):
        response = self.client.get(reverse('mark_notification_read', args=[self.notif1.id]))
        self.assertEqual(response.status_code, 302)
        self.notif1.refresh_from_db()
        self.assertTrue(self.notif1.is_read)

    def test_mark_all_notifications_read(self):
        response = self.client.get(reverse('mark_all_notifications_read'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notification.objects.filter(student=self.student, is_read=False).count(), 0)

    def test_delete_notification(self):
        response = self.client.get(reverse('delete_notification', args=[self.notif1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Notification.objects.filter(id=self.notif1.id).exists())


from django.core.files.uploadedfile import SimpleUploadedFile
from user_management.forms import StudentForm, StudentProfileEditForm


class StudentFieldValidationTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'registration_number': 'MEA22MCA100',
            'name': 'Valid Student',
            'email': 'valid@meaec.edu.in',
            'phone': '+91 9876543210',
            'course': 'MCA',
            'username': 'validstudent',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
        }

    def test_valid_student_form_passes(self):
        form = StudentForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['phone'], '9876543210')
        self.assertEqual(form.cleaned_data['email'], 'valid@meaec.edu.in')

    def test_invalid_name_rejected(self):
        # Digits only in name
        data = self.valid_data.copy()
        data['name'] = '123456'
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

        # Symbols only in name
        data['name'] = '@@$$%%'
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_invalid_phone_rejected(self):
        data = self.valid_data.copy()
        data['phone'] = '123'  # Too short
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

        data['phone'] = '1234567890'  # 10 digits but starts with 1 (not 6,7,8,9)
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

        data['phone'] = 'abcdefghij'  # Alphabetic
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_invalid_course_rejected(self):
        data = self.valid_data.copy()
        data['course'] = 'NonExistentCourse'
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('course', form.errors)

        data['course'] = ''
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('course', form.errors)

    def test_invalid_registration_number_rejected(self):
        data = self.valid_data.copy()
        data['registration_number'] = 'AB'  # Too short
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('registration_number', form.errors)

        data['registration_number'] = 'MEA@22#MCA'  # Invalid symbols
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('registration_number', form.errors)

    def test_duplicate_email_rejected(self):
        Student.objects.create(
            registration_number='MEA22MCA001',
            name='First Student',
            email='alreadyexists@meaec.edu.in',
            phone='9876543210',
            course='MCA'
        )
        data = self.valid_data.copy()
        data['email'] = 'alreadyexists@meaec.edu.in'
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_short_password_rejected(self):
        data = self.valid_data.copy()
        data['password'] = 'short'
        data['confirm_password'] = 'short'
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_resume_file_extension_validation(self):
        # Valid PDF file
        pdf_file = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test resume content", content_type="application/pdf")
        form = StudentForm(data=self.valid_data, files={'resume': pdf_file})
        self.assertTrue(form.is_valid(), form.errors)

        # Invalid .exe file
        exe_file = SimpleUploadedFile("script.exe", b"binary content", content_type="application/x-msdownload")
        form = StudentForm(data=self.valid_data, files={'resume': exe_file})
        self.assertFalse(form.is_valid())
        self.assertIn('resume', form.errors)

