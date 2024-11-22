
from django.contrib import admin
from apps.helpers import models as coreModels


# Register your models here.


class AdminHelper(admin.ModelAdmin):
    list_display = ("id","file","is_active")

admin.site.register(coreModels.FileUpload, AdminHelper)


class DropDownMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
admin.site.register(coreModels.DropdownMaster, DropDownMasterAdmin)


class DropDownValuesAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "dropdownmaster")

admin.site.register(coreModels.DropdownValues, DropDownValuesAdmin)
