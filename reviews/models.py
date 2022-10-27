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
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "like_reviews")


class Comment(models.Model):
    title = models.CharField(max_length=80)
    content = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE)
