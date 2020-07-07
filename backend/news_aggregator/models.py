from django.db import models

# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=400)
    image_url=models.URLField(max_length=500)
    blog_url=models.URLField(max_length=600)
    def __str__(self):
        return self.title