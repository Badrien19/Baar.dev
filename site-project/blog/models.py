from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Game(models.Model):
    winner = models.ForeignKey(Profile, null=True, on_delete= models.SET_NULL, related_name='winner')
    looser = models.ForeignKey(Profile, null=True, on_delete= models.SET_NULL, related_name='looser')
    ratio = models.IntegerField(default=20)
    draw = models.BooleanField(default = False)
    date = models.DateTimeField(default=timezone.now, blank=True)
    stat_winner = models.FloatField(default='0', blank=True)
    stat_looser = models.FloatField(default='0', blank=True)

