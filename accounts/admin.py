from django.contrib import admin

from .models import *

admin.site.register(Technician)

class InspectionImageAdmin(admin.StackedInline):
    model = InspectionImage

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    inlines = [InspectionImageAdmin]

    class Meta:
       model = Inspection

@admin.register(InspectionImage)
class InspectionImageAdmin(admin.ModelAdmin):
    pass