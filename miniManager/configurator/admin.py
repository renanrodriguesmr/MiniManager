from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Configuration)

admin.site.register(Measure)

admin.site.register(Measurement)