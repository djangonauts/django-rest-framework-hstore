from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework.fields import WritableField

from django_hstore.dict import HStoreDict
from django_hstore.exceptions import HStoreDictException


__all__ = ['HStoreField']


class HStoreField(WritableField):
    """
    DRF HStore Dictionary Field
    """
    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop('schema', False)
        super(HStoreField, self).__init__(*args, **kwargs)
        if self.schema:
            # hide dictionary field, use virtual fields
            self.write_only = True
            self.read_only = True
    
    def from_native(self, value):
        if value:
            try:
                return HStoreDict(value)
            except HStoreDictException as e:
                raise ValidationError(_('Invalid JSON: %s' % e.json_error_message))
        else:
            return None

    def to_native(self, value):
        if isinstance(value, dict) or value is None:
            return value
        
        value = HStoreDict(value)

        return value
