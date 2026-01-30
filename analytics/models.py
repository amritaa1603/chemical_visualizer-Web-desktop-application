from django.db import models

class EquipmentDataset(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary_data = models.JSONField()  # Stores the calculated stats

    def __str__(self):
        return self.file_name