from django.urls import reverse
from rest_framework import status
import pytest
from model_bakery import baker

from api.models import Material


@pytest.fixture
def user_material(user_patient):
    return baker.make(Material, patient_id=user_patient.id)

@pytest.fixture
def admin_material(admin_patient):
    return baker.make(Material, patient_id=admin_patient.id)


@pytest.mark.django_db
class TestMaterialCreate:
    @classmethod
    def get_url(cls, patient_pk):
        return reverse('material-list', kwargs={'patient_pk': patient_pk})

    def test_if_user_anonymous_returns_401(self, client, user_patient):
        url = self.get_url(user_patient.id)
        response = client.post(url, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_non_exist_parent_patient_404(self, admin_client):
        url = self.get_url(99999)
        response = admin_client.post(url, data={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_non_relative_parent_patient_404(self, user_client, admin_patient):
        url = self.get_url(admin_patient.id)
        response = user_client.post(url, adata={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_non_relative_with_non_admin_user_404(self, user_client, admin_patient):
        url = self.get_url(admin_patient.id)
        response = user_client.post(url, data={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_success_post_relative_with_non_admin_user(self, user_client, user_patient):
        url = self.get_url(user_patient.id)
        with open('api/tests/X-ray.jpg', 'rb') as file:
            response = user_client.post(url, data={"file": file}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
   

@pytest.mark.django_db
class TestMaterialList:
    @classmethod
    def get_url(cls, patient_pk):
        return reverse('material-list', kwargs={'patient_pk': patient_pk})

    def test_if_user_anonymous_returns_401(self, client, user_patient):
        url = self.get_url(user_patient.id)
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_exist_parent_patient_404(self, admin_client):
        url = self.get_url(99999)
        response = admin_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_non_relative_parent_patient_404(self, user_client, admin_patient):
        url = self.get_url(admin_patient.id)
        response = user_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_seccess_get_all_if_admin_user(self, admin_client, user_patient):
        url = self.get_url(user_patient.id)
        response = admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_non_relative_with_non_admin_user_404(self, user_client, admin_patient):
        url = self.get_url(admin_patient.id)
        response = user_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_success_get_relative_with_non_admin_user(self, user_client, user_patient):
        url = self.get_url(user_patient.id)
        response = user_client.get(url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveMaterial:
    @classmethod
    def get_url(cls, patient_pk, material_pk):
        return reverse(
            'material-detail',
            kwargs={
                'patient_pk': patient_pk,
                'pk': material_pk
            }
        )
    
    def test_if_user_anonymous_returns_401(self, client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_exist_parent_patient_404(self, admin_client):
        url = self.get_url(99999, 1)
        response = admin_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_non_relative_parent_patient_404(self, user_client, admin_patient, user_material):
        url = self.get_url(admin_patient.id, user_material.id)
        response = user_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_success_retrieve_related(self, user_client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        response = user_client.get(url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestMaterialUpdate:

    @classmethod
    def get_url(cls, patient_pk, material_pk):
        return reverse(
            'material-detail',
            kwargs={
                'patient_pk': patient_pk,
                'pk': material_pk
            }
        )
    
    def test_if_user_anonymous_returns_401(self, client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        response = client.put(url, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_exist_parent_patient_404(self, admin_client):
        url = self.get_url(99999, 1)
        response = admin_client.put(url, data={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_non_relative_parent_patient_404(self, user_client, admin_patient, admin_material):
        url = self.get_url(admin_patient.id, admin_material.id)
        response = user_client.put(url, data={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_success_update_with_admin_user(self, admin_client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        old_filename = user_material.file.name

        with open('api/tests/X-ray.jpg', 'rb') as file:
            response = admin_client.put(url, data={'file': file})

        assert response.status_code == status.HTTP_200_OK
        user_material.refresh_from_db()
        assert user_material.file.name != old_filename

    def test_success_update_with_not_admin_user(self, user_client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        old_filename = user_material.file.name

        with open('api/tests/X-ray.jpg', 'rb') as file:
            response = user_client.put(url, data={'file': file})

        assert response.status_code == status.HTTP_200_OK
        user_material.refresh_from_db()
        assert user_material.file.name != old_filename


@pytest.mark.django_db
class TestDeleteMaterial:
    @classmethod
    def get_url(cls, patient_pk, material_pk):
        return reverse(
            'material-detail',
            kwargs={
                'patient_pk': patient_pk,
                'pk': material_pk
            }
        )

    def test_if_user_anonymous_returns_401(self, client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        response = client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_success_delete_with_admin_user(self, admin_client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Material.objects.filter(id=user_material.id).exists()

    def test_success_delete_with_not_admin_user(self, user_client, user_patient, user_material):
        url = self.get_url(user_patient.id, user_material.id)
        response = user_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Material.objects.filter(id=user_material.id).exists()