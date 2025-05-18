from django.db import models

# Create your models here.

class TemporaryData(models.Model):
    name = models.CharField(max_length=255)
    thumbnailLink = models.URLField()
    item_weight = models.FloatField()
    time_date = models.DateTimeField()
    camera_flag = models.BooleanField(default=False)
    mcu_flag = models.BooleanField(default=False)
    weight_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class ImageClassificationResult(models.Model):
    image_name = models.CharField(max_length=255)
    classification_flag = models.CharField(max_length=50)
    classification_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name