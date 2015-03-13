from django.db import models
from django_hstore import hstore
import datetime


__all__ = [
    'DataBag',
    'SchemaDataBag'
]


class HStoreModel(models.Model):
    objects = hstore.HStoreManager()

    class Meta:
        abstract = True


class DataBag(HStoreModel):
    name = models.CharField(max_length=32)
    data = hstore.DictionaryField()


class SchemaDataBag(HStoreModel):
    name = models.CharField(max_length=32)
    data = hstore.DictionaryField(schema=[
        {
            'name': 'number',
            'class': 'IntegerField',
            'kwargs': {
                'default': 1
            }
        },
        {
            'name': 'float',
            'class': models.FloatField,
            'kwargs': {
                'default': 1.0
            }
        },
        {
            'name': 'boolean',
            'class': 'BooleanField',
            'kwargs': {
                'default': False
            }
        },
        {
            'name': 'boolean_true',
            'class': 'BooleanField',
            'kwargs': {
                'verbose_name': 'boolean true',
                'default': True
            }
        },
        {
            'name': 'char',
            'class': 'CharField',
            'kwargs': {
                'default': 'test', 'blank': True, 'max_length': 10
            }
        },
        {
            'name': 'text',
            'class': 'TextField',
            'kwargs': {
                'blank': True
            }
        },
        {
            'name': 'choice',
            'class': 'CharField',
            'kwargs': {
                'blank': True,
                'max_length': 10,
                'choices': (('choice1', 'choice1'), ('choice2', 'choice2')),
                'default': 'choice1'
            }
        },
        {
            'name': 'choice2',
            'class': 'CharField',
            'kwargs': {
                'blank': True,
                'max_length': 10,
                'choices': (('choice1', 'choice1'), ('choice2', 'choice2')),
            }
        },
        {
            'name': 'date',
            'class': 'DateField',
            'kwargs': {
                'blank': True,
                'default': datetime.date(2015, 3, 15),
            }
        },
        {
            'name': 'datetime',
            'class': 'DateTimeField',
            'kwargs': {
                'blank': True
            }
        },
        {
            'name': 'decimal',
            'class': 'DecimalField',
            'kwargs': {
                'blank': True,
                'decimal_places': 2,
                'max_digits': 4,
                'default': '1.0',
            }
        },
        {
            'name': 'email',
            'class': 'EmailField',
            'kwargs': {
                'blank': True
            }
        },
        {
            'name': 'ip',
            'class': 'GenericIPAddressField',
            'kwargs': {
                'blank': True,
                'null': True
            }
        },
        {
            'name': 'url',
            'class': models.URLField,
            'kwargs': {
                'blank': True
            }
        },
    ])
