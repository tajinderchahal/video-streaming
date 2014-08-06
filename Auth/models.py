from django.db import models
from django.contrib.auth.models import User

class ArtCategory(models.Model):
    category = models.CharField(max_length=100)

class UserProfile(User):
    source = models.CharField(max_length=20)
    no_of_videos = models.IntegerField(default=0)
    # V for viewer, M for manager, A for artist, C for curator
    user_type = models.CharField(max_length=1)
    art_category = models.ForeignKey(ArtCategory, null=True, blank=True)

class RendezvousUser(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    user_code = models.IntegerField(null=True, blank=True)
