# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('tourist', '游客'),
        ('guide', '导游'),
        ('travel_agency', '旅行社'),
        ('tourism_bureau', '文旅局'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class TravelAgency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='travel_agency')
    agency_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.agency_name

    class Meta:
        verbose_name = '旅行社'
        verbose_name_plural = '旅行社'


class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide')
    guide_id = models.CharField(max_length=50)
    travel_agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, related_name='guides')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '导游'
        verbose_name_plural = '导游'