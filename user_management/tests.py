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
        self.assertEqual(student.name, 'Test Student')
        self.assertEqual(student.course, 'MCA')

        # Verify welcome notification
        self.assertTrue(Notification.objects.filter(student=student).exists())

    def test_registration_password_mismatch(self):
        data = {
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

    def test_profile_edit(self):
        # Test editing profile without requiring password
        response = self.client.post(reverse('student_edit_self'), {
            'name': 'Updated Profile Name',
            'email': 'updated@test.com',
            'phone': '9999999999',
            'course': 'M.Tech CSE'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        self.student.refresh_from_db()
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
