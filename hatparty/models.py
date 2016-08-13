from django.db import models
from django.utils import timezone
from rest_framework import serializers

import uuid


class Hat(models.Model):
    name = models.CharField(max_length=255)
    image_file = models.FilePathField(blank=True, null=True)
    description = models.TextField()

    @property
    def current_wearer(self):
        try:
            return self._current_wearer
        except Exception:
            return None


class HatUser(models.Model):
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    counter_value = models.IntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False)
    current_hat = models.OneToOneField(
        Hat, related_name='_current_wearer', blank=True, null=True)


class Like(models.Model):
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(HatUser, related_name='created_likes')
    target_user = models.ForeignKey(HatUser, related_name='current_likes')
    hat = models.ForeignKey(Hat, related_name='current_likes')


class Slap(models.Model):
    create_date = models.DateTimeField(default=timezone.now)
    create_user = models.ForeignKey(HatUser, related_name='created_slaps')
    target_user = models.ForeignKey(HatUser, related_name='current_slaps')


class HatTransfer(models.Model):
    create_date = models.DateTimeField(default=timezone.now)
    source_user = models.ForeignKey(HatUser, related_name='transfers_from')
    target_user = models.ForeignKey(
        HatUser, related_name='transfers_to', blank=True, null=True)
    hat = models.ForeignKey(Hat, related_name='transfers')


class HatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hat


class HatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HatUser


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like


class SlapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slap


class HatTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = HatTransfer
