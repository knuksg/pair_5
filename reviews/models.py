from django.db import models
from django.conf import settings
# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    movie_title = models.CharField(max_length=100)
    content = models.TextField()
    grade = models.IntegerField()
    image = models.ImageField(upload_to="reviews/", blank=True)