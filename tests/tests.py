import json
import datetime

from django.test import TestCase

from .models import *
from .serializers import *
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from .views import SchemaDataBagViewSet


class TestDjangoRestFrameworkHStore(TestCase):
    def test_hstore_field_serializer(self):
        d = DataBag()
        d.name = 'test'
        d.data['a'] = 'a'
        d.data['b'] = 'b'
        d.full_clean()
        d.save()

        s = DataBagSerializer(instance=d).data

        self.assertEqual(s['data'], {'a': 'a', 'b': 'b'})

    def test_hstore_field_api_create_string(self):
        response = self.client.post('/databag/', {
            "name": "test",
            "data": '{ "a": "a", "b": "b" }'
        })
        self.assertEqual(response.status_code, 201)

        d = DataBag.objects.last()
        self.assertEqual(d.name, 'test')
        self.assertEqual(d.data, {'a': 'a', 'b': 'b'})

    def test_hstore_field_api_create_json(self):
        post_data = {
            "name": "test",
            "data": {'a': 'a', 'b': 2}
        }
        response = self.client.post('/databag/', json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        d = DataBag.objects.last()
        self.assertEqual(d.name, 'test')
        self.assertEqual(d.data, {'a': 'a', 'b': '2'})

    def test_hstore_field_api_validation_error(self):
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

    def test_hstore_serializer(self):
        d = SchemaDataBag()
        d.name = 'test'
        d.number = 2
        d.float = 2.2
        d.boolean = True
        d.boolean_true = False
        d.char = 'char'
        d.text = 'text'
        d.date = datetime.date.today()
        d.datetime = datetime.datetime.now()
        d.decimal = 2.0
        d.email = 'test@test.com'
        d.ip = '10.10.10.10'
        d.url = 'http://test.com'
        d.full_clean()
        d.save()

        s = SchemaDataBagSerializer(instance=d).data

        self.assertEqual(s['name'], 'test')
        self.assertEqual(s['number'], 2)
        self.assertEqual(s['float'], 2.2)
        self.assertIs(s['boolean'], True)
        self.assertIs(s['boolean_true'], False)
        self.assertEqual(s['char'], 'char')
        self.assertEqual(s['text'], 'text')
        self.assertEqual(s['date'], str(d.date))
        self.assertEqual(s['datetime'], str(d.datetime.isoformat()))
        self.assertEqual(s['decimal'], '2.00')
        self.assertEqual(s['email'], 'test@test.com')
        self.assertEqual(s['ip'], '10.10.10.10')
        self.assertEqual(s['url'], 'http://test.com')
        # should be hidden
        self.assertTrue('data' not in s)

    def test_hstore_serializer_validation(self):
        obj = SchemaDataBag()
        data = {
            "name": "test create",
            "number": 'c',
            "float": 2.2,
            "boolean": True,
            "boolean_true": False,
            "char": "char",
            "text": "test create text",
            "choice": "choice2",
            "choice2": "choice1",
            "date": "2014-08-08",
            "datetime": "2014-08-08 14:10:53",
            "decimal": 1.0,
            "email": "WRONG",
            "ip": "10.10.10.10",
            "url": "WRONG"
        }

        s = SchemaDataBagSerializer(instance=obj, data=data)
        self.assertFalse(s.is_valid())
        self.assertTrue('email' in s.errors)
        self.assertTrue('number' in s.errors)
        self.assertTrue('url' in s.errors)

        data['email'] = 'test@test.com'
        data['number'] = 4
        data['url'] = 'http://test.com'
        s = SchemaDataBagSerializer(instance=obj, data=data)
        self.assertTrue(s.is_valid())

    def test_hstore_serializer_default(self):
        obj = SchemaDataBag()
        data = {
            "name": "test create",
        }

        s = SchemaDataBagSerializer(instance=obj, data=data)
        self.assertTrue(s.is_valid())
        s = s.data

        self.assertEqual(s['number'], 1)
        self.assertEqual(s['float'], 1.0)
        self.assertEqual(s['boolean_true'], True)
        self.assertEqual(s['char'], 'test')
        self.assertEqual(s['text'], '')
        self.assertEqual(s['choice'], 'choice1')


class TestDjangoRestFrameworkHStoreAPI(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_hstore_serializer_api(self):
        response = self.client.get('/schemadatabag/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/schemadatabag/', HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<select')
        self.assertContains(response, 'type="checkbox"')

    def create_schema_data_bag(self):
        response = self.client.post(reverse('schemadatabag-list'), {
            "name": "test create",
            "number": 2,
            "float": 2.2,
            "boolean": True,
            "boolean_true": False,
            "char": "char",
            "text": "test create text",
            "choice": "choice2",
            "choice2": "choice1",
            "date": "2014-08-08",
            "datetime": "2014-08-08 14:10:53+00:00",
            "decimal": 1.0,
            "email": "test@test.com",
            "ip": "10.10.10.10",
            "url": "http://test.com"
        })
        return response

    def test_hstore_serializer_api_create(self):
        response = self.create_schema_data_bag()

        self.assertEqual(response.status_code, 201)

        d = SchemaDataBag.objects.last()
        self.assertEqual(d.name, 'test create')
        self.assertEqual(d.number, 2)
        self.assertEqual(d.float, 2.2)
        self.assertEqual(d.boolean, True)
        self.assertEqual(d.boolean_true, False)
        self.assertEqual(d.char, 'char')
        self.assertEqual(d.text, 'test create text')
        self.assertEqual(d.choice, 'choice2')
        self.assertEqual(d.choice2, 'choice1')
        self.assertEqual(str(d.date), '2014-08-08')
        self.assertEqual(str(d.datetime), '2014-08-08 14:10:53+00:00')
        self.assertEqual(d.decimal, 1.0)
        self.assertEqual(d.email, 'test@test.com')
        self.assertEqual(d.ip, '10.10.10.10')
        self.assertEqual(d.url, 'http://test.com')

    def test_hstore_serializer_api_update(self):
        view = SchemaDataBagViewSet.as_view(actions={'put': 'update'})

        response = self.create_schema_data_bag()
        self.assertIn('id', response.data)
        bag_id = response.data['id']

        request = self.factory.put(reverse('schemadatabag-detail', args=(bag_id,)), data={
            "name": "test update",
            "number": 5,
            "float": 5.2,
            "boolean": True,
            "boolean_true": False,
            "char": "char",
            "text": "test update text",
            "choice": "choice2",
            "choice2": "choice1",
            "date": "2014-08-08",
            "datetime": "2014-08-08 14:10:53+00:00",
            "decimal": 5.0,
            "email": "test@test.com",
            "ip": "10.10.10.10",
            "url": "http://test.com"
        })
        response = view(request, pk=bag_id)
        self.assertEqual(response.status_code, 200)

        d = SchemaDataBag.objects.last()
        self.assertEqual(d.name, 'test update')
        self.assertEqual(d.number, 5)
        self.assertEqual(d.float, 5.2)
        self.assertEqual(d.boolean, True)
        self.assertEqual(d.boolean_true, False)
        self.assertEqual(d.char, 'char')
        self.assertEqual(d.text, 'test update text')
        self.assertEqual(d.choice, 'choice2')
        self.assertEqual(d.choice2, 'choice1')
        self.assertEqual(str(d.date), '2014-08-08')
        self.assertEqual(str(d.datetime), '2014-08-08 14:10:53+00:00')
        self.assertEqual(d.decimal, 5.0)
        self.assertEqual(d.email, 'test@test.com')
        self.assertEqual(d.ip, '10.10.10.10')
        self.assertEqual(d.url, 'http://test.com')

    def test_hstore_serializer_api_create_default(self):
        response = self.client.post('/schemadatabag/', {
            "name": "test default",
        })

        self.assertEqual(response.status_code, 201)

        d = SchemaDataBag.objects.last()
        self.assertEqual(d.name, 'test default')
        self.assertEqual(d.number, 1)
        self.assertEqual(d.float, 1.0)
        self.assertEqual(d.boolean, False)
        self.assertEqual(d.boolean_true, True)
        self.assertEqual(d.char, 'test')
        self.assertEqual(d.text, '')
        self.assertEqual(d.choice, 'choice1')
