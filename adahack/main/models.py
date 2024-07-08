from django.db import models

# Create your models here.


class IIIFManifest(models.Model):
    manifest = models.JSONField()
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', default='uploads/manifest.json')
    created_at = models.DateTimeField(auto_now_add=True)
