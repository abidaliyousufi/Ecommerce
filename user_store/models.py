from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Products(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  description = models.TextField()
  image = models.ImageField(upload_to='images/')
  price = models.IntegerField()


class Comments(models.Model):
  comment = models.TextField()
  user = models.ForeignKey(User,on_delete = models.CASCADE)
  product_id = models.ForeignKey(Products,on_delete = models.CASCADE)