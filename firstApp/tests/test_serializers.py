from rest_framework.test import APITestCase
from firstApp.models import Potato
from TestProject.RESTApiGen.serializers import get_serializer
from django.forms.models import model_to_dict



class TestAppModel(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = Potato
        cls.model.objects.create()
        cls.model.objects.create(status='A')
        cls.model.objects.create(description='description1')
        cls.model.objects.create(status='B', description='description2')

    def test_create_object(self):
        def_object = self.model.objects.first()
        a_object = self.model.objects.get(status='A')
        desc_object = self.model.objects.get(description='description1')
        hybrid_object = self.model.objects.get(status='B', description='description2')

        self.assertEqual(def_object.status, 'New')
        self.assertEqual(def_object.description, f'{self.model.__name__} object')
        self.assertEqual(a_object.status, 'A')
        self.assertEqual(a_object.description, f'{self.model.__name__} object')
        self.assertEqual(desc_object.status, 'New')
        self.assertEqual(desc_object.description, 'description1')
        self.assertEqual(hybrid_object.status, 'B')
        self.assertEqual(hybrid_object.description, 'description2')

    def test_serializer_with_empty_data(self):
        serializer = get_serializer(self.model)(data={})
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_valid_data(self):
        object_data = model_to_dict(self.model.objects.first())
        serializer = get_serializer(self.model)(data=object_data)
        self.assertTrue(serializer.is_valid())
