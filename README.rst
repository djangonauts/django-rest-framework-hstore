Django Rest Framework HStore
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://travis-ci.org/djangonauts/django-rest-framework-hstore.png
   :target: https://travis-ci.org/djangonauts/django-rest-framework-hstore

.. image:: https://coveralls.io/repos/djangonauts/django-rest-framework-hstore/badge.png
  :target: https://coveralls.io/r/djangonauts/django-rest-framework-hstore

.. image:: https://landscape.io/github/djangonauts/django-rest-framework-hstore/master/landscape.png
   :target: https://landscape.io/github/djangonauts/django-rest-framework-hstore/master
   :alt: Code Health

.. image:: https://requires.io/github/djangonauts/django-rest-framework-hstore/requirements.png?branch=master
   :target: https://requires.io/github/djangonauts/django-rest-framework-hstore/requirements/?branch=master
   :alt: Requirements Status

------------

Serializer field for django-hstore.

This code was originally written for `Nodeshot <https://github.com/ninuxorg/nodeshot>`__
and then extracted into this generic python package.

HStoreField
===========

Not sufficient to support schema mode.

.. code-block:: python

    from rest_framework import serializers
    from myapp.models import MyModel
    
    # rest_framework_hstore 
    from rest_framework_hstore.fields import HStoreField
    
    class MyHStoreSerializer(serializers.ModelSerializer):
        data = HStoreField()
        
        class Meta:
            model = MyModel


HStoreSerializer
================

Supports ``DictionaryField`` and schema mode out of the box.

.. code-block:: python

    from myapp.models import MyModel
    
    # rest_framework_hstore 
    from rest_framework_hstore.serializers import HStoreSerializer
    
    class MyHStoreSerializer(HStoreSerializer):
        class Meta:
            model = MyModel
