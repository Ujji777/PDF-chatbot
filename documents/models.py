from django.db import models

class UploadedDocument(models.Model):
    file = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True, null=True)  # Optional
    uploaded_at = models.DateTimeField(auto_now_add=True)
