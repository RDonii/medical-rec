from django.urls import reverse
from rest_framework import status
from model_bakery import baker
import pytest

from api.models import Patient

@pytest.fixture
def user_patient(user):
    return baker.make(Patient, doctor=user.profile)

@pytest.fixture
def admin_patient(admin_user):
    return baker.make(Patient, doctor=admin_user.profile)


@pytest.mark.django_db
class TestCreatePatient:
    url = reverse('patient-list')

    def test_if_user_anonymous_returns_401(self, client):
        response = client.post(self.url, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_admin_doctor_required(self, admin_client, patient_data):
        response = admin_client.post(self.url, data=patient_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_success_creation_with_admin_user(self, admin_client, user, patient_data):
        patient_data['doctor'] = user.profile.id

        response = admin_client.post(self.url, data=patient_data)

        assert response.status_code == status.HTTP_201_CREATED
    
    def test_success_creation_with_not_admin_user(self, user_client, user, patient_data):
        response = user_client.post(self.url, data=patient_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Patient.objects.get(id=response.data['id']).doctor_id == user.profile.id


@pytest.mark.django_db
class TestListPatient:
    url = reverse('patient-list')

    def test_if_user_anonymous_returns_401(self, client):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_admin_get_all(self, admin_client, admin_user, user):
        baker.make(Patient, 3, doctor=user.profile)
        baker.make(Patient, 3, doctor=admin_user.profile)

        response = admin_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 6

    def test_if_user_not_admin_get_only_relateds(self, user_client, admin_user, user):
        related_patients_num = 3    # make sure number of maked patients less than pagination number: related + non_related < page_size
        related_patients = baker.make(Patient, related_patients_num, doctor=user.profile)
        related_idxs = (patient.id for patient in related_patients)     # generator to search related idx, make list if need to store in memory
        baker.make(Patient, 3, doctor=admin_user.profile)

        response = user_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == related_patients_num
        assert len(list(map(lambda x: x['id'] in related_idxs, response.data["results"]))) == related_patients_num


@pytest.mark.django_db
class TestRetrievePatient:
    url_name = 'patient-detail'

    def test_if_user_anonymous_returns_401(self, client, user):
        response = client.get(reverse(self.url_name, args=[user.id]))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_not_admin_404_for_non_related(self, user_client, admin_patient):
        response = user_client.get(reverse(self.url_name, args=[admin_patient.id]))

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_success_retrieve_related(self, user_client, user, user_patient):
        response = user_client.get(reverse(self.url_name, args=[user_patient.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user_patient.id


@pytest.mark.django_db
class TestUpdatePatient:
    url_name = 'patient-detail'

    # PUT tests

    def test_put_if_user_anonymous_returns_401(self, client, user_patient):
        response = client.put(reverse(self.url_name, args=[user_patient.id]), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_if_user_admin_doctor_required(self, admin_client, user_patient, patient_data):
        response = admin_client.put(reverse(self.url_name, args=[user_patient.id]), data=patient_data)
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_success_put_with_admin_user(self, admin_client, user, user_patient, patient_data):
        patient_data['doctor'] = user.profile.id

        response = admin_client.put(reverse(self.url_name, args=[user_patient.id]), data=patient_data)

        assert response.status_code == status.HTTP_200_OK
        user_patient.refresh_from_db()
        assert user_patient.first_name == patient_data["first_name"]
        assert user_patient.last_name == patient_data["last_name"]
        assert str(user_patient.birth_date) == patient_data["birth_date"]
        assert user_patient.gender == patient_data["gender"]
        assert user_patient.med_condition == patient_data["med_condition"]
        assert user_patient.doctor_id == user.profile.id
    
    def test_success_put_with_not_admin_user(self, user_client, user, patient_data, user_patient):
        response = user_client.put(reverse(self.url_name, args=[user_patient.id]), data=patient_data)

        assert response.status_code == status.HTTP_200_OK
        user_patient.refresh_from_db()
        assert user_patient.first_name == patient_data["first_name"]
        assert user_patient.last_name == patient_data["last_name"]
        assert str(user_patient.birth_date) == patient_data["birth_date"]
        assert user_patient.gender == patient_data["gender"]
        assert user_patient.med_condition == patient_data["med_condition"]
        assert user_patient.doctor_id == user.profile.id

    # PATCH tests

    def test_patch_if_user_anonymous_returns_401(self, client, user_patient):
        response = client.patch(reverse(self.url_name, args=[user_patient.id]), data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_success_patch_with_admin_user(self, admin_client, user, user_patient):
        old_data = {
            "last_name": user_patient.last_name,
            "birth_date": str(user_patient.birth_date),
            "med_condition": user_patient.med_condition,
        }
        change_data = {
            "first_name": "updated name",
            "gender": "M"
        }

        response = admin_client.patch(reverse(self.url_name, args=[user_patient.id]), data=change_data)

        assert response.status_code == status.HTTP_200_OK
        user_patient.refresh_from_db()
        assert user_patient.first_name == "updated name"
        assert user_patient.gender == "M"
        assert user_patient.last_name == old_data["last_name"]
        assert str(user_patient.birth_date) == old_data["birth_date"]
        assert user_patient.med_condition == old_data["med_condition"]
        assert user_patient.doctor_id == user.profile.id
    
    def test_success_patch_with_not_admin_user(self, user_client, user, user_patient):
        old_data = {
            "last_name": user_patient.last_name,
            "birth_date": str(user_patient.birth_date),
            "med_condition": user_patient.med_condition,
        }
        change_data = {
            "first_name": "updated name",
            "gender": "M"
        }

        response = user_client.patch(reverse(self.url_name, args=[user_patient.id]), data=change_data)

        assert response.status_code == status.HTTP_200_OK
        user_patient.refresh_from_db()
        assert user_patient.first_name == "updated name"
        assert user_patient.gender == "M"
        assert user_patient.last_name == old_data["last_name"]
        assert str(user_patient.birth_date) == old_data["birth_date"]
        assert user_patient.med_condition == old_data["med_condition"]
        assert user_patient.doctor_id == user.profile.id