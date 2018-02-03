from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# @admin.register(Rate)
# class RateAdmin(ImportExportModelAdmin):
#     pass

admin.site.register(Subtype)
admin.site.register(Agent)
admin.site.register(Sale)
admin.site.register(Led)
admin.site.register(SaleLed)
admin.site.register(Utility)
admin.site.register(Zone)
admin.site.register(ServiceClass)
admin.site.register(RetailEnergyProvider)
admin.site.register(Team)
