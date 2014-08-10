from rest_framework.serializers import ModelSerializer


__all__ = ['HStoreSerializer']


class _FieldMappingDict(dict):
    def __getitem__(self, *args, **kwargs):
        """
        in case of virtual hstore fields, the argument won't match any key because
        virtual field classes don't match exactly standard django model field classes
        but it will match the string key
        """
        args = list(args)
        cls = args[0]
        
        # if class doesn't match any class in the keys, but its string representation does
        if cls not in self.keys() and cls.__name__ in self.keys():
            # substitute argument with string instead of concrete class
            args[0] = cls.__name__
        
        return super(_FieldMappingDict, self).__getitem__(*args, **kwargs)


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
        
        This approach is taken in order to avoid overriding the get_field method,
        this should give us the advantage of less mantainance in the long run,
        while the disadvantage of complexity is small because the few lines of code.
        """
        # iterate over self.field_mapping
        for model_field, serializer_field in self.field_mapping.items():
            # if the field can be represented as a string
            if hasattr(model_field, '__name__'):
                # add mapping using string instead of class
                self.field_mapping[model_field.__name__] = serializer_field
        
        # override self.field_mapping with a custom dict class
        self.field_mapping = _FieldMappingDict(self.field_mapping)
    
    def restore_object(self, attrs, instance=None):
        """
        temporarily remove hstore virtual fields otherwise DRF considers them many2many
        """
        model = self.opts.model
        meta = self.opts.model._meta
        original_virtual_fields = list(meta.virtual_fields)  # copy
        
        # remove hstore virtual fields from meta
        for field in model._hstore_virtual_fields.values():
            meta.virtual_fields.remove(field)
        
        instance = super(HStoreSerializer, self).restore_object(attrs, instance)
        
        # restore original virtual fields
        meta.virtual_fields = original_virtual_fields
        
        return instance
