from django.contrib import admin
from .models import UploadedDefectFile

@admin.register(UploadedDefectFile)
class UploadedDefectFileAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'uploaded_at')
