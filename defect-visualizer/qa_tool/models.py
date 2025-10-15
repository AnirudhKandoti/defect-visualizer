from django.db import models

class UploadedDefectFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.original_name or self.file.name} ({self.uploaded_at:%Y-%m-%d %H:%M})"
