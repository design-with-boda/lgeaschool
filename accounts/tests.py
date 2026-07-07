from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AdminLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='adminuser',
            password='StrongPass123',
            email='admin@example.com',
            is_staff=True,
        )

    def test_admin_dashboard_requires_login(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/?next=/admin-dashboard/', response.url)

    def test_admin_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'adminuser', 'password': 'StrongPass123', 'remember_me': 'on'},
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin_dashboard'))
