from django.db import models
from django.contrib.auth.models import User
from storages.backends.gcloud import GoogleCloudStorage

# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp} - {self.user_input}'

class Psychologist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tipo_consulta = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    correo = models.EmailField()
    numero = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='psychologists_photos/', blank=True, null=True, storage=GoogleCloudStorage())

    def __str__(self):
        return self.name
    
    def get_photo_url(self):
        return self.photo.url