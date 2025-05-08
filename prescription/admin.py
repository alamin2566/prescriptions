from django.contrib import admin
from .models import Prescription, HeaderFooter

admin.site.register(Prescription)
admin.site.register(HeaderFooter)

from .models import TemplateData

admin.site.register(TemplateData)
