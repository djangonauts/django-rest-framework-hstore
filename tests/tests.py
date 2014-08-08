import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import *
from .serializers import *


class TestHStoreField(TestCase):
    def test_databag(self):
        d = DataBag()
        d.name = 'test'
        d.data['a'] = 'a'
        d.data['b'] = 'b'
        d.full_clean()
        d.save()
        
        s = DataBagSerializer(instance=d).data
        
        self.assertEqual(s['data'], { 'a': 'a', 'b': 'b' })
    
    def test_databag_serializer_api_create_string(self):
        response = self.client.post('/databag/', {
            "name": "test", 
            "data": '{ "a": "a", "b": "b" }'
        })
        self.assertEqual(response.status_code, 201)
        
        d = DataBag.objects.last()
        self.assertEqual(d.name, 'test')
        self.assertEqual(d.data, { 'a': 'a', 'b': 'b' })
    
    def test_databag_serializer_api_create_json(self):
        post_data = {
            "name": "test", 
            "data": { 'a': 'a', 'b': 2 }
        }
        response = self.client.post('/databag/', json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        d = DataBag.objects.last()
        self.assertEqual(d.name, 'test')
        self.assertEqual(d.data, { 'a': 'a', 'b': '2' })
    
    def test_databag_serializer_api_validation_error(self):
        response = self.client.post('/databag/', {
            "name": "test", 
            "data": "{ WRONG }"
        })
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post('/databag/', {
            "name": "test", 
            "data": "true"
        })
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post('/databag/', {
            "name": "test", 
            "data": "1"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_schemadatabag_serializer(self):
        d = SchemaDataBag()
        d.name = 'test'
        d.number = 2
        d.float = 2.2
        d.boolean = True
        d.full_clean()
        d.save()
        
        s = SchemaDataBagSerializer(instance=d).data
        
        self.assertEqual(s['name'], 'test')
        self.assertEqual(s['number'], 2)
        self.assertEqual(s['float'], 2.2)
        self.assertIs(s['boolean'], True)
        # should be hidden
        self.assertTrue('data' not in s)
    
    def test_schemadatabag_serializer_api(self):
        response = self.client.get('/schemadatabag/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/schemadatabag/', HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_schemadatabag_serializer_api_create(self):     
        response = self.client.post('/schemadatabag/', {
            "name": "test", 
            "number": 2,
            "float": 2.2,
            "date": "2014-08-08",
            "boolean": 1,
            "boolean_true": 0,
            "decimal": "1.0"
        })
        self.assertEqual(response.status_code, 201)
        
        d = SchemaDataBag.objects.last()
        self.assertEqual(d.name, 'test')
        self.assertEqual(d.number, 2)
        self.assertEqual(d.float, 2.2)
    
    def test_schemahstore_api(self):
        response = self.client.get('/schemahstore/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/schemahstore/', HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<select')
        self.assertContains(response, 'type="checkbox"')
    
    def test_schemahstore_serializer_api_create(self):     
        response = self.client.post('/schemahstore/', {
            "name": "test", 
            "number": 2,
            "float": 2.2,
            "date": "2014-08-08",
            "boolean": True,
            "boolean_true": False,
            "decimal": 1.0
        })
        self.assertEqual(response.status_code, 201)
        
        d = SchemaDataBag.objects.last()
        self.assertEqual(d.name, 'test')
        self.assertEqual(d.number, 2)
        self.assertEqual(d.float, 2.2)
        self.assertEqual(d.boolean, True)
        self.assertEqual(d.boolean_true, False)
        self.assertEqual(d.char, 'test')
        self.assertEqual(d.decimal, 1.0)
