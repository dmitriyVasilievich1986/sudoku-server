from rest_framework.test import APIClient
from account.models import Account
from django.test import TestCase
import json

API_URL = "http://localhost/api/account/"

TEST_CREATE_USERNAME = "root"
TEST_USER_USERNAME = "test"


class AccountTestModel(TestCase):
    def setUp(self):
        self.client = APIClient()
        obj: Account = Account.create(
            username=TEST_USER_USERNAME, password=TEST_USER_USERNAME)
        obj.save()
        self.token = f"token {obj.token}"
        self._id = obj.id

    def test_api_create(self):
        data = {"username": TEST_CREATE_USERNAME,
                "password": TEST_CREATE_USERNAME}
        response = self.client.post(API_URL, data=data)
        self.assertEqual(response.status_code, 201)

    def test_api_create_fail(self):
        data = {"username": TEST_USER_USERNAME, "password": TEST_USER_USERNAME}
        response = self.client.post(API_URL, data=data)
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            API_URL, data={"username": TEST_CREATE_USERNAME})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            API_URL, data={"password": TEST_CREATE_USERNAME})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(API_URL)
        self.assertEqual(response.status_code, 400)

    def test_api_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(API_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("username"), TEST_USER_USERNAME)

    def test_api_get_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="token wrong token")
        response = self.client.get(API_URL)
        self.assertEqual(response.status_code, 403)
        response = self.client.get(f"{API_URL}{self._id}/")
        self.assertEqual(response.status_code, 405)

    def test_api_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(
            f"{API_URL}{self._id}/", data=json.dumps({"name": "name"}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "name")
        response = self.client.patch(
            f"{API_URL}{self._id}/", data=json.dumps({"surname": "surname"}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["surname"], "surname")
        response = self.client.patch(
            f"{API_URL}{self._id}/", data=json.dumps({"dificulty": 10}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("dificulty"), 10)
        response = self.client.patch(
            f"{API_URL}{self._id}/", data=json.dumps({"help": False}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("help"), False)

    def test_api_login(self):
        data = json.dumps({"username": TEST_USER_USERNAME,
                          "password": TEST_USER_USERNAME})
        response = self.client.post(
            f"{API_URL}login/", data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.token = f"token {response.json().get('token')}"

    def test_api_login_fail(self):
        data = json.dumps({"username": TEST_CREATE_USERNAME,
                          "password": TEST_CREATE_USERNAME})
        response = self.client.post(
            f"{API_URL}login/", data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_api_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(f"{API_URL}logout/")
        self.assertEqual(response.status_code, 204)

    def test_api_logout_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="token wrong token")
        response = self.client.get(f"{API_URL}logout/")
        self.assertEqual(response.status_code, 403)
