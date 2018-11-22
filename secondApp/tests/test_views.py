from rest_framework.test import APITestCase
from secondApp.models import Tomato
from TestProject.RESTApiGen.serializers import get_serializer
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from functools import partial

class TestAppVies(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = Tomato
        cls.model.objects.create()
        cls.model.objects.create(status='A')
        cls.model.objects.create(description='description1')
        cls.model.objects.create(status='B', description='description2')

        cls.url = f'{cls.model.__name__.lower()}'

    def test_get_object(self):
        url = reverse(f'{self.url}-detail', kwargs={'pk':1})
        response = self.client.get(url)
        true_obj = self.model.objects.get(pk=1)
        serializer = get_serializer(self.model)(true_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_objects(self):
        url = reverse(f'{self.url}-list')
        response = self.client.get(url)

        true_obj = self.model.objects.all()
        serializer = get_serializer(self.model)(true_obj, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_objects(self):
        # single field filtering
        url = reverse(f'{self.url}-list')
        url += f"?{urlencode({'status':'New'})}"
        response = self.client.get(url)

        true_obj = self.model.objects.filter(status='New')
        serializer = get_serializer(self.model)(true_obj, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # AND logic
        url = reverse(f'{self.url}-list')
        url += f"?{urlencode({'status':'B', 'description':'description2'})}"
        response = self.client.get(url)

        true_obj = self.model.objects.filter(status='B', description='description2')
        serializer = get_serializer(self.model)(true_obj, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_limit_list(self):
        url = reverse(f'{self.url}-list')
        url += f"?{urlencode({'limit':3})}"
        response = self.client.get(url)

        true_obj = self.model.objects.all()[:3]
        serializer = get_serializer(self.model)(true_obj, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sort_list(self):
        url = reverse(f'{self.url}-list')
        url += f"?{urlencode({'sort':'status'})}"
        response = self.client.get(url)

        true_obj = self.model.objects.all().order_by('status')
        serializer = get_serializer(self.model)(true_obj, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_object(self):
        url = reverse(f'{self.url}-list')
        response = self.client.post(url, data={'status':'Ab', 'description':'Test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_object(self):
        url = reverse(f'{self.url}-detail', kwargs={'pk':1})
        response = self.client.put(url, data={'status':'Ok', 'description':'Something'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = self.model.objects.get(pk=1)
        self.assertEqual(model_to_dict(obj), {'status':'Ok', 'description':'Something', 'id':1})

    def test_delete_object(self):
        url = reverse(f'{self.url}-detail', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        callable = partial(self.model.objects.get, pk=1)
        self.assertRaises(ObjectDoesNotExist, callable)
