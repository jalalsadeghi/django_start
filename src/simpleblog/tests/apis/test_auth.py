import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
import json

@pytest.mark.django_db
def test_login():
    user = User.objects.create_user(
       username='JalalTest' , password="Jalal123!@#", email="jalaltest@gmail.com"
    )

    client = APIClient()
    url_ = reverse("api:auth:jwt:login")
    body = {"username": "JalalTest", "password": "Jalal123!@#"}
    response = client.post(url_, json.dumps(body), content_type="application/json")
    auth = json.loads(response.content)
    access = auth.get("access")
    refresh = auth.get("refresh")

    assert access != None
    assert type(access) == str

    assert refresh != None
    assert type(refresh) == str
