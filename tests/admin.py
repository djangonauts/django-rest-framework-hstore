from django.contrib import admin
from .models import *


class DataBagAdmin(admin.ModelAdmin):
    list_display = ['name']


class SchemaDataBagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(DataBag, DataBagAdmin)
admin.site.register(SchemaDataBag, SchemaDataBagAdmin)
