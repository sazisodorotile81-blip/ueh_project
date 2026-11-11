from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, ServiceRequest

class PlatformAPITests(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username="msme", password="StrongPass123!", role="CLIENT")
        self.agent = User.objects.create_user(username="agent", password="StrongPass123!", role="AGENT")
    def test_client_can_create_request(self):
        self.client.force_authenticate(self.client_user)
        response = self.client.post("/api/requests/", {
            "category": "FUNDING", "description": "I need help preparing a funding application.", "urgency": "MEDIUM"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceRequest.objects.count(), 1)
    def test_client_cannot_change_status(self):
        obj = ServiceRequest.objects.create(client=self.client_user, category="OTHER", description="Need business support please.", urgency="LOW")
        self.client.force_authenticate(self.client_user)
        response = self.client.patch(f"/api/requests/{obj.id}/", {"status": "RESOLVED"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_registration_defaults_to_client(self):
        response = self.client.post("/api/auth/register/", {
            "username": "newclient", "email": "new@example.com", "password": "LongStrongPass123!"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="newclient").role, "CLIENT")
