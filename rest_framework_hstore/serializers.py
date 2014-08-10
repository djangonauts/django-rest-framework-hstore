from django.db import models
from django.forms import widgets

from rest_framework.fields import * 
from rest_framework.serializers import ModelSerializer

from django_hstore.fields import DictionaryField

from .fields import HStoreField


__all__ = ['HStoreSerializer']


class HStoreSerializer(ModelSerializer):
    """
    Better support for django-hstore schema mode
    to django-rest-framework
    """
    def __init__(self, *args, **kwargs):
        self.__map_virtual_fields()
        super(HStoreSerializer, self).__init__(*args, **kwargs)
    
    def __map_virtual_fields(self):
        """
        the standard DRF field_mapping uses model field classes as keys:
        
        field_mapping = {
            ...
            models.DateField: DateField,
            ...
        }
        
        we need to add strings with the name of the classes to the mapping:
        
        field_mapping = {
            ...
            models.DateField: DateField,
            "models.DateField": DateField,
            ...
        }
        
        The reason is that a virtual field won't match the standard django field,
        but can match the string version.
        """
        # add DictionaryField to field_mapping
        self.field_mapping[DictionaryField] = HStoreField
        # TODO: support ReferenceField
        
        additional_fields = {}
        # iterate over self.field_mapping
        for field_class, serializer_field in self.field_mapping.items():
            # if the field can be represented as a string
            if hasattr(field_class, '__name__'):
                # add mapping using string instead of class
                additional_fields[field_class.__name__] = serializer_field
        
        # update field_mapping dictionary
        self.field_mapping.update(additional_fields)
    
    def get_field(self, model_field):
        """
        Creates a default instance of a basic non-relational field.
        """
        kwargs = {}

        if model_field.null or model_field.blank:
            kwargs['required'] = False

        if isinstance(model_field, models.AutoField) or not model_field.editable:
            kwargs['read_only'] = True

        if model_field.has_default():
            kwargs['default'] = model_field.get_default()

        if issubclass(model_field.__class__, models.TextField):
            kwargs['widget'] = widgets.Textarea

        if model_field.verbose_name is not None:
            kwargs['label'] = model_field.verbose_name

        if model_field.help_text is not None:
            kwargs['help_text'] = model_field.help_text

        # TODO: TypedChoiceField?
        if model_field.flatchoices:  # This ModelField contains choices
            kwargs['choices'] = model_field.flatchoices
            if model_field.null:
                kwargs['empty'] = None
            return ChoiceField(**kwargs)

        # put this below the ChoiceField because min_value isn't a valid initializer
        if issubclass(model_field.__class__, models.PositiveIntegerField) or\
                issubclass(model_field.__class__, models.PositiveSmallIntegerField):
            kwargs['min_value'] = 0

        attribute_dict = {
            models.CharField: ['max_length'],
            models.CommaSeparatedIntegerField: ['max_length'],
            models.DecimalField: ['max_digits', 'decimal_places'],
            models.EmailField: ['max_length'],
            models.FileField: ['max_length'],
            models.ImageField: ['max_length'],
            models.SlugField: ['max_length'],
            models.URLField: ['max_length'],
        }

        if model_field.__class__ in attribute_dict:
            attributes = attribute_dict[model_field.__class__]
            for attribute in attributes:
                kwargs.update({attribute: getattr(model_field, attribute)})
        
        if model_field.__class__ == DictionaryField and model_field.schema:
            kwargs['schema'] = True

        try:
            return self.field_mapping[model_field.__class__](**kwargs)
        except KeyError:
            pass
        
        try:
            return self.field_mapping[model_field.__class__.__name__](**kwargs)
        except KeyError:
            return ModelField(model_field=model_field, **kwargs)
    
    def restore_object(self, attrs, instance=None):
        """
        temporarily remove hstore virtual fields otherwise DRF considers them many2many
        """
        model = self.opts.model
        meta = self.opts.model._meta
        original_virtual_fields = list(meta.virtual_fields)  # copy
        
        if hasattr(model, '_hstore_virtual_fields'):
            # remove hstore virtual fields from meta
            for field in model._hstore_virtual_fields.values():
                meta.virtual_fields.remove(field)
            
        instance = super(HStoreSerializer, self).restore_object(attrs, instance)
        
        if hasattr(model, '_hstore_virtual_fields'):
            # restore original virtual fields
            meta.virtual_fields = original_virtual_fields
        
        return instance
