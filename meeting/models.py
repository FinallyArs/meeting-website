from datetime import timedelta, date, datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.postgres.fields import JSONField
import base64
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.conf import settings

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, get_language



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    last_login = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.FileField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    MALE = 'Male'
    FEMALE = 'Female'
    NEUTRAL = 'Neutral'
    SELECT_GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NEUTRAL, 'Neutral')
    )
    FRIENDSHIP = 'Friendship'
    INTIMATE = 'Intimate'

    SELECT_RELATIONSHIP = (
        (FRIENDSHIP, 'Friendship'),
        (INTIMATE, 'Intimate')
    )
    gender = models.CharField(
        max_length=10,
        choices=SELECT_GENDER,
        default='Select'
    )
    relation = models.CharField(
        max_length=10,
        choices=SELECT_RELATIONSHIP,
        default='Select'
    )
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    last_online = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    def __str__(self):
        return str(self.user) if self.user else ''

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.pk])

    def total_likes(self):
        return self.likes.count()

    def age(self):
        return int((datetime.now().date() - self.birth_date).days / 365.25)

    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
        return False

    def get_online_info(self):
        if self.is_online():
            return 'Online'
        if self.last_online:
            return 'Last visit {}'.format(naturaltime(self.last_online))
        return 'Unknown'




class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG)
    members = models.ManyToManyField(Profile)


    def get_absolute_url(self):
        return 'meeting:messages', (), {'chat_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    is_readed = models.BooleanField(default=False)

    class Meta:
        ordering=['pub_date']

    def __str__(self):
        return self.message








