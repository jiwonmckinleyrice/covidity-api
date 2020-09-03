from django.contrib import admin
from api.models import ConfirmedCase, District

class ConfirmedCaseAdmin(admin.ModelAdmin):
    model = ConfirmedCase
    list_display = ["id", "count", "district", "created_at"]


class DistrictAdmin(admin.ModelAdmin):
    model = District
    list_display = ["id", "name", "created_at"]

admin.site.register(ConfirmedCase, ConfirmedCaseAdmin)
admin.site.register(District, DistrictAdmin)
