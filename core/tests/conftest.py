from rest_framework.test import APIClient
import pytest


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def new_user_data():
    return {
        "username": "testusername",
        "password": "testpassword123"
    }