from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework import status


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(
            email="user0@example.com",
            username="test0",
            first_name="test0",
            last_name="user0",
            phone_number="0712345689",
            password="password",
        )

    def test_create_user(self):
        data = {
            "email": "user1@example.com",
            "username": "test1",
            "first_name": "test1",
            "last_name": "user1",
            "phone_number": "07125680092",
            "password": "password",
            "re_password": "password",
        }
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertTrue(CustomUser.objects.filter(email="user1@example.com").exists())

    def test_get_user_list(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)


    def test_get_user_detail(self):
        response = self.client.get(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        data = {"email": "updated@example.com", "first_name": "updated name"}
        response = self.client.patch(f"/api/v1/users/{self.user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")

    def test_delete_user(self):
        response = self.client.delete(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertFalse(
            CustomUser.objects.filter(email="updated@example.com").exists()
        )
        
        
# class LoginViewTestCase(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             email="tetsuser@example.com",
#             username="testuser",
#             first_name="test0",
#             last_name="user0",
#             phone_number="0712345689",
#             password="password",
#         )
#         self.login_url = "/api/v1/login/"
#         self.client = APIClient()

#     def test_login(self):
#         data = {
#             "email": "tetsuser@example.com",
#             "password": "password",
#         }
#         response = self.client.post(self.login_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("token", response.data)
#         self.assertEqual(response.cookies["token"].value, response.data["token"])

#     def test_login_invalid_credentials(self):
#         data = {
#             "email": "test9990@example.com",
#             "password": "invalidpassword",
#         }
#         response = self.client.post(self.login_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertTrue("error" in response.data)


# class LogoutViewTestCase(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             email="testuser2@example.com",
#             password="password",
#             username="testuser2",
#             first_name="test",
#             last_name="user",
#             phone_number="0712345679",
#         )
#         self.client = APIClient()

#     def test_logout_success(self):
#         # Authenticate the user by creating a token
#         token, _ = Token.objects.get_or_create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

#         # Logout the user
#         response = self.client.post("/api/v1/users/logout/", format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Logged out successfully')

#     def test_logout_failure_unauthenticated(self):
#         response = self.client.post("/api/v1/users/logout/", format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)