from django.db import models

# Create your models here.

# class History(models.Model):
#     title = models.CharField(max_length=200)
#     json = models.FileField(upload_to='histories/json/')

#     def __str__(self):
#         return str(self.title)


# class Video(models.Model):
#     title = models.CharField(max_length=200)
#     URL = models.CharField(max_length=200)
#     time = models.DateTimeField(auto_now=False)
#     videoID = models.CharField(max_length=100) #correct for youtube video id max length
#     categoryID = models.PositiveIntegerField() #consider matching categoryID with category name in video model

#     def __str__(self):
#         return str(self.title)